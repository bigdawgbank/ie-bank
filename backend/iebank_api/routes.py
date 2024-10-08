from flask import Flask, jsonify, request

from iebank_api import app, db
from iebank_api.models import Account


@app.route("/accounts", methods=["POST"])
def create_account():
    name = request.json.get("name")
    currency = request.json.get("currency")
    country = request.json.get("country")

    if not name:
        return jsonify({"error": "Name cannot be empty."}), 400
    if not currency:
        return jsonify({"error": "Currency cannot be empty or None."}), 400
    if not country:
        return jsonify({"error": "Country cannot be empty."}), 400

    account = Account(name, currency, country)

    db.session.add(account)
    db.session.commit()
    return jsonify(format_account(account)), 201


@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    return jsonify({"accounts": [format_account(account) for account in accounts]}), 200


@app.route("/accounts/<int:id>", methods=["GET"])
def get_account(id):
    account = Account.query.get(id)
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["PUT"])
def update_account(id):
    account = Account.query.get(id)
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    account.name = name
    db.session.commit()
    return jsonify(format_account(account)), 200


@app.route("/accounts/<int:id>", methods=["DELETE"])
def delete_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account cannot be empty"}), 400
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
        "created_at": account.created_at,
    }
