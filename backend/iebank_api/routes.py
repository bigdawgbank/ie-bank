from datetime import datetime, timezone
from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from iebank_api import app, bcrypt, db
from iebank_api.models import Account, BankTransfer, Role, User


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        current_user = db.session.get(User, user_id)

        if not current_user or current_user.role != Role.ADMIN:
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)

    return decorated_function


# Get all users (Admin only)
@app.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    users = db.session.query(User).all()
    return (
        jsonify(
            {
                "users": [
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "account_count": user.accounts.count(),
                    }
                    for user in users
                ]
            }
        ),
        200,
    )


# Get specific user details (Admin only)
@app.route("/users/<int:user_id>", methods=["GET"])
@admin_required
def get_user_details(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "accounts": [
                    {
                        "id": account.id,
                        "name": account.name,
                        "balance": account.balance,
                        "currency": account.currency,
                        "status": account.status,
                        "country": account.country,
                        "created_at": account.created_at.isoformat(),
                    }
                    for account in user.get_accounts()
                ],
            }
        ),
        200,
    )


# Create new user (Admin only)
@app.route("/users", methods=["POST"])
@admin_required
def create_user():
    data = request.json

    try:
        new_user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=Role.USER.value,
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": {
                        "id": new_user.id,
                        "username": new_user.username,
                        "email": new_user.email,
                        "role": new_user.role,
                    },
                }
            ),
            201,
        )

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {str(e)}")
        return jsonify({"error": "Failed to create user"}), 500


# Update user (Admin only)
@app.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    try:
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.set_password(data["password"])
        if "role" in data:
            user.role = data["role"]

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    },
                }
            ),
            200,
        )

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user: {str(e)}")
        return jsonify({"error": "Failed to update user"}), 500


# Delete user (Admin only)
@app.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    current_admin_id = int(get_jwt_identity())
    if current_admin_id == user_id:
        return jsonify({"error": "Cannot delete your own admin account"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User and all associated accounts deleted successfully",
                    "deleted_user_id": user_id,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {str(e)}")
        return jsonify({"error": "Failed to delete user"}), 500


# Change user's account status (Admin only)
@app.route("/users/<int:user_id>/accounts/<int:account_id>/status", methods=["PATCH"])
@admin_required
def update_account_status(user_id, account_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    account = (
        db.session.query(Account).filter_by(id=account_id, user_id=user_id).first()
    )
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.json
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "New status is required"}), 400

    try:
        account.status = new_status
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Account status updated successfully",
                    "account": {
                        "id": account.id,
                        "name": account.name,
                        "status": account.status,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error updating account status: {str(e)}")
        return jsonify({"error": "Failed to update account status"}), 500


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
        return jsonify({"error": "Registration failed"}), 500


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = db.session.query(User).filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,  # Make sure to include the role
            }
        ),
        200,
    )


@app.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    data = request.json

    if not data:
        return jsonify({"error": "Provide data"}), 400

    name = data.get("name")
    currency = data.get("currency")
    country = data.get("country")
    balance = data.get("balance")

    if not name:
        return jsonify({"error": "Name cannot be empty."}), 400
    if not currency:
        return jsonify({"error": "Currency cannot be empty or None."}), 400
    if not country:
        return jsonify({"error": "Country cannot be empty."}), 400
    if not balance:
        balance = 0

    # Create account and associate with current user
    account = Account(name, currency, country, user, balance)
    db.session.add(account)
    db.session.commit()

    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
@jwt_required()
def get_accounts():
    user_id = int(get_jwt_identity())
    # Only get accounts belonging to current user
    accounts = db.session.query(Account).filter_by(user_id=user_id).all()
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
@jwt_required()
def get_account(id):
    user_id = int(get_jwt_identity())
    account = Account.query.get_or_404(id)
    # Check if account belongs to current user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(format_account(account)), 200


@app.route("/accounts/<string:account_name>", methods=["GET"])
@jwt_required()
def get_account_by_name(account_name):
    account = Account.query.filter_by(name=account_name).first()
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
@jwt_required()
def update_account(id):
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
    account = db.session.get(Account, id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    # Check if account belongs to current user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(account)
    db.session.commit()
    return jsonify(format_account(account)), 200


def format_account(account: Account):
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


@app.route("/transfer", methods=["POST"])
@jwt_required()
def transfer_money():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    data = request.get_json()
    from_account_id = data.get("sender_account_id")
    to_account_id = data.get("recipient_account_id")
    amount = data.get("amount")

    if not from_account_id or not to_account_id or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    from_account = db.session.get(Account, from_account_id)
    to_account = db.session.get(Account, to_account_id)

    if not from_account or not to_account:
        return jsonify({"error": "Invalid account details"}), 400

    if from_account.user_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        bank_transfer = BankTransfer(from_account, to_account, amount)
        bank_transfer.process_transfer()
        return (
            jsonify(
                {
                    "message": "Transfer successful",
                    "receipt": {
                        "sender_account_id": from_account.id,
                        "recipient_account_id": to_account.id,
                        "amount": amount,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
