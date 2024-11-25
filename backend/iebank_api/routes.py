from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from iebank_api import app, bcrypt, db
from iebank_api.models import Account, User


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Form validation
    if not username:
        return jsonify({"message": "Missing username field"}), 400
    if not email:
        return jsonify({"message": "Missing email field"}), 400
    if not password:
        return jsonify({"message": "Missing password field"}), 400

    # Password strength validation
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters"}), 400
    if not any(c.isupper() for c in password):
        return jsonify({"message": "Password must contain uppercase letter"}), 400
    if not any(c.islower() for c in password):
        return jsonify({"message": "Password must contain lowercase letter"}), 400
    if not any(c.isdigit() for c in password):
        return jsonify({"message": "Password must contain a number"}), 400

    try:
        # Try to create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except ValueError as e:
        # Handle validation errors from the model
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        # Handle any other unexpected errors
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({"message": "Registration failed"}), 500


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = db.session.query(User).filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    data = request.json

    if not data:
        return jsonify({"message": "Provide data"}), 400

    name = data.get("name")
    currency = data.get("currency")
    country = data.get("country")

    if not name:
        return jsonify({"error": "Name cannot be empty."}), 400
    if not currency:
        return jsonify({"error": "Currency cannot be empty or None."}), 400
    if not country:
        return jsonify({"error": "Country cannot be empty."}), 400

    # Create account and associate with current user
    account = Account(name, currency, country, user)
    db.session.add(account)
    db.session.commit()

    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    # Only get accounts belonging to current user
    accounts = db.session.query(Account).filter_by(user_id=user_id).all()
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
@jwt_required()
def get_account(id):
    user_id = get_jwt_identity()
    account = Account.query.get_or_404(id)
    # Check if account belongs to current user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
@jwt_required()
def update_account(id):
    user_id = get_jwt_identity()
    account = db.session.get(Account, id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    # Check if account belongs to current user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    account.name = name
    db.session.commit()
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_account(id):
    user_id = get_jwt_identity()
    account = db.session.get(Account, id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    # Check if account belongs to current user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(account)
    db.session.commit()
    return jsonify(format_account(account)), 200


def format_account(account):
    return {
        "id": account.id,
        "name": account.name,
        "account_number": account.account_number,
        "balance": account.balance,
        "currency": account.currency,
        "status": account.status,
        "country": account.country,
        "created_at": account.created_at.isoformat(),
        "user_id": account.user_id,  # Added user_id to response
    }


# Optional: Add route to get user profile with accounts
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        ),
        200,
    )
