from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity  # Added these imports
from iebank_api import app, db
from iebank_api.models import Account, User, BankTransfer  # Added `User` and `BankTransfer` import
from iebank_api.__init__ import logger  # Use the logger configured in __init__.py
from datetime import datetime, timezone  # Added missing imports for datetime and timezone


@app.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    data = request.json

    if not data:
        return jsonify({"message": "Provide data"}), 400

    name = data.get("name")
    currency = data.get("currency")
    country = data.get("country")
    balance = data.get("balance")

    if not name:
        logger.warning("Account creation failed: 'name' is missing")
        return jsonify({"error": "Name cannot be empty."}), 400
    if not currency:
        logger.warning("Account creation failed: 'currency' is missing")
        return jsonify({"error": "Currency cannot be empty or None."}), 400
    if not country:
        logger.warning("Account creation failed: 'country' is missing")
        return jsonify({"error": "Country cannot be empty."}), 400
    if not balance:
        balance = 0

    account = Account(name, currency, country)
    db.session.add(account)
    db.session.commit()

    logger.info(f"Account created successfully: {format_account(account)}")
    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
@jwt_required()
def get_accounts():
    accounts = Account.query.all()
    logger.info(f"Retrieved {len(accounts)} accounts")
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
@jwt_required()
def get_account(id):
    account = Account.query.get(id)
    if not account:
        logger.warning(f"Account retrieval failed: ID {id} not found")
        return jsonify({"error": "Account not found"}), 404

    logger.info(f"Retrieved account: {format_account(account)}")
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
@jwt_required()
def update_account(id):
    account = Account.query.get(id)
    if not account:
        logger.warning(f"Account update failed: ID {id} not found")
        return jsonify({"error": "Account not found"}), 404

    name = request.json.get("name")
    if not name:
        logger.warning("Account update failed: 'name' is missing")
        return jsonify({"error": "Name cannot be empty"}), 400

    account.name = name
    db.session.commit()

    logger.info(f"Account updated successfully: {format_account(account)}")
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_account(id):
    user_id = int(get_jwt_identity())
    account = db.session.get(Account, id)
    if not account:
        logger.warning(f"Account deletion failed: ID {id} not found")
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()

    logger.info(f"Account deleted successfully: ID {id}")
    return jsonify({"message": "Account deleted"}), 200


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
