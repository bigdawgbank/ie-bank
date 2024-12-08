import pytest
from iebank_api import app
import json
from unittest.mock import patch, mock_open

def test_create_account(testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    # Create account
    response = testing_client.post("/accounts", 
                                  json={"name": "My Savings Account", "currency": "€", "country": "Ireland"}, 
                                  headers=headers)

    assert response.status_code == 201
    assert response.json["name"] == "My Savings Account"
    assert response.json["currency"] == "€"
    assert response.json["country"] == "Ireland"
    assert "account_number" in response.json
    assert "user_id" in response.json

    # Verify account in list
    accounts_response = testing_client.get("/accounts", headers=headers)
    assert accounts_response.status_code == 200
    accounts = accounts_response.json.get("accounts", accounts_response.json)
    assert len(accounts) == 1
    assert accounts[0]["name"] == "My Savings Account"


def test_create_account_invalid_data(testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}

    # Test missing name
    response = testing_client.post(
        "/accounts", json={"currency": "€", "country": "Ireland"}, headers=headers
    )
    assert response.status_code == 400
    assert "error" in response.json

    # Test missing currency
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "country": "Ireland"}, headers=headers
    )
    assert response.status_code == 400
    assert "error" in response.json

    # Test missing country
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "currency": "€"}, headers=headers
    )
    assert response.status_code == 400
    assert "error" in response.json


def test_create_account_unauthorized(testing_client):
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "currency": "€", "country": "Ireland"}
    )
    assert response.status_code == 401

def test_get_accounts(testing_client, register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}

    # Test protected route with token
    response = testing_client.get("/accounts", headers=headers)
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get("/wrong_path")
        assert response.status_code == 404

def test_get_account_by_account_id(testing_client, register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}

    # Query all existing accounts
    response_all = testing_client.get('/accounts', headers=headers)
    assert response_all.status_code == 200

    # Parse the JSON response
    accounts = json.loads(response_all.data)
    
    # Ensure there are accounts in the response
    assert len(accounts['accounts']) > 0

    # Get the first account
    first_account = accounts['accounts'][0]
    
    # Perform assertions on the first account
    assert 'id' in first_account
    assert 'account_number' in first_account
    assert 'name' in first_account
    assert 'currency' in first_account
    assert 'country' in first_account

    # Now we can test get by account number
    response_single = testing_client.get('/accounts/' + str(first_account['id']), headers=headers)
    assert response_single.status_code == 200

# test update/put to the by default account id=1
def test_put_account(testing_client ,register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is updated (PUT)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}

    response = testing_client.put('/accounts/1', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'}, headers=headers)
    assert response.status_code == 200

# test_delete_account would delete the by default created account with id=1
def test_delete_account(testing_client, register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is deleted (DELETE)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.delete('/accounts/1', headers=headers)
    assert response.status_code == 200

def test_bank_transfer_process_route(testing_client, register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/transfer' page is requested (POST)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    sender_account_name = "Adrian checking account"
    recipient_account_name = "Daniel checking account"
    response = testing_client.post("/accounts", 
                                  json={"name": sender_account_name, "currency": "€", "country": "Spain", "balance": 1000.0}, 
                                  headers=headers)
    response = testing_client.post("/accounts", 
                                  json={"name": recipient_account_name, "currency": "€", "country": "Spain", "balance": 0.0}, 
                                  headers=headers)

    response_sender_account = testing_client.get(f"/accounts/{sender_account_name}", headers=headers)
    # Parse the JSON response
    sender_account_data = response_sender_account.get_json()
    # Extract the account ID
    from_account_id = sender_account_data['id']

    response_recipient_account = testing_client.get(f"/accounts/{recipient_account_name}", headers=headers)
    # Parse the JSON response
    recipient_account_data = response_recipient_account.get_json()
    # Extract the account ID
    to_account_id = recipient_account_data['id']

    response = testing_client.post('/transfer', json={'sender_account_id': from_account_id, 'recipient_account_id': to_account_id, 'amount': 100.0}, headers=headers)
    assert response.status_code == 200

def test_wire_transfer_money_route(testing_client, register_and_authenticate):
    """
    GIVEN a Flask application
    WHEN the '/wiretransfer' page is requested (POST)
    THEN check the response is valid
    """
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    sender_account_name = "Adrian checking account"
    recipient_account_name = "Daniel checking account"

    # Create sender account
    response = testing_client.post(
        "/accounts",
        json={"name": sender_account_name, "currency": "€", "country": "Spain", "balance": 1000.0},
        headers=headers,
    )
    assert response.status_code == 201
    sender_account_data = response.get_json()
    from_account_id = sender_account_data["id"]

    # Create recipient account
    response = testing_client.post(
        "/accounts",
        json={"name": recipient_account_name, "currency": "€", "country": "Spain", "balance": 0.0},
        headers=headers,
    )
    assert response.status_code == 201
    recipient_account_data = response.get_json()
    recipient_account_number = recipient_account_data["account_number"]

    # Perform wire transfer
    response = testing_client.post(
        "/wiretransfer",
        json={"sender_account_id": from_account_id, "recipient_account_number": recipient_account_number, "amount": 100.0},
        headers=headers,
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Wire Transfer successful"
    assert response_data["receipt"]["sender_account_id"] == from_account_id
    assert response_data["receipt"]["recipient_account_id"] == recipient_account_data["id"]
    assert response_data["receipt"]["amount"] == 100.0

@patch('builtins.open', new_callable=mock_open, read_data='{"exchange_rate": {"USD_TO_EURO_EXCHANGE_RATE": "0.95"}}')
def test_get_exchange_rate_usd_to_eur(mock_file, testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/exchangerate?from_currency=$&to_currency=€", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['from_currency'] == '$'
    assert data['to_currency'] == '€'
    assert data['exchange_rate'] == 0.95

@patch('builtins.open', new_callable=mock_open, read_data='{"exchange_rate": {"USD_TO_EURO_EXCHANGE_RATE": "0.95"}}')
def test_get_exchange_rate_eur_to_usd(mock_file, testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/exchangerate?from_currency=€&to_currency=$", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['from_currency'] == '€'
    assert data['to_currency'] == '$'
    assert data['exchange_rate'] == round(1 / 0.95, 2)

def test_get_exchange_rate_missing_from_currency(testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/exchangerate?to_currency=USD", headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_get_exchange_rate_missing_to_currency(testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/exchangerate?from_currency=USD", headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

@patch('iebank_api.models.os.getenv')
def test_get_exchange_rate_same_currency(mock_getenv, testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/exchangerate?from_currency=USD&to_currency=USD", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['from_currency'] == 'USD'
    assert data['to_currency'] == 'USD'
    assert data['exchange_rate'] == 1