from flask import jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from iebank_api import app, bcrypt, db, login_manager
from iebank_api.models import Account, User


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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

    # Check if user exists
    if db.session.query(User).filter_by(username=username).first() and db.session.query(
        User
    ).filter_by(email=email):
        return jsonify({"message": "User already exists"}), 400

    # Create new user
    new_user = User(username=username, email=email, password=password)
    print(f"new_user{new_user}")
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = db.session.query(User).filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Account does not exist"}), 401


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/session", methods=["GET"])
def check_session():
    if current_user.is_authenticated:
        return jsonify({"authenticated": True}), 200
    return jsonify({"message": False}), 401


@app.route("/accounts", methods=["POST"])
@login_required
def create_account():
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
    account = Account(name, currency, country, current_user)
    db.session.add(account)
    db.session.commit()

    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
@login_required
def get_accounts():
    # Only get accounts belonging to current user
    accounts = db.session.query(Account).filter_by(user_id=current_user.id).all()
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
@login_required
def get_account(id):
    account = Account.query.get_or_404(id)
    # Check if account belongs to current user
    if account.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
@login_required
def update_account(id):
    account = db.session.get(Account, id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    # Check if account belongs to current user
    if account.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    account.name = name
    db.session.commit()
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["DELETE"])
@login_required
def delete_account(id):
    account = db.session.get(Account, id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    # Check if account belongs to current user
    if account.user_id != current_user.id:
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
@login_required
def get_profile():
    return (
        jsonify(
            {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "accounts": [
                    format_account(account) for account in current_user.get_accounts()
                ],
            }
        ),
        200,
    )
