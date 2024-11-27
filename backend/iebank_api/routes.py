from flask import Flask, jsonify, request
from iebank_api import app, db
from iebank_api.models import Account
from iebank_api.__init__ import logger  # Use the logger configured in __init__.py


@app.route("/accounts", methods=["POST"])
def create_account():
    name = request.json.get("name")
    currency = request.json.get("currency")
    country = request.json.get("country")

    if not name:
        logger.warning("Account creation failed: 'name' is missing")
        return jsonify({"error": "Name cannot be empty."}), 400
    if not currency:
        logger.warning("Account creation failed: 'currency' is missing")
        return jsonify({"error": "Currency cannot be empty or None."}), 400
    if not country:
        logger.warning("Account creation failed: 'country' is missing")
        return jsonify({"error": "Country cannot be empty."}), 400

    account = Account(name, currency, country)
    db.session.add(account)
    db.session.commit()

    logger.info(f"Account created successfully: {format_account(account)}")
    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    logger.info(f"Retrieved {len(accounts)} accounts")
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
def get_account(id):
    account = Account.query.get(id)
    if not account:
        logger.warning(f"Account retrieval failed: ID {id} not found")
        return jsonify({"error": "Account not found"}), 404

    logger.info(f"Retrieved account: {format_account(account)}")
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
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
def delete_account(id):
    account = Account.query.get(id)
    if not account:
        logger.warning(f"Account deletion failed: ID {id} not found")
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()

    logger.info(f"Account deleted successfully: ID {id}")
    return jsonify({"message": "Account deleted"}), 200


def format_account(account):
    return {
        "id": account.id,
        "name": account.name,
        "account_number": account.account_number,
        "balance": account.balance,
        "currency": account.currency,
        "status": account.status,
        "country": account.country,
        "created_at": account.created_at,
    }
