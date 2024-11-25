import pytest
from iebank_api import app
import json

def test_create_account(testing_client):
    # Register and login
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )
    response = testing_client.post(
        "/login", data={"username": "testuser", "password": "TestPass123"}
    )
    token = response.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    response = testing_client.post(
        "/accounts",
        json={"name": "My Savings Account", "currency": "€", "country": "Ireland"},
        headers=headers,
    )
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


def test_create_account_invalid_data(testing_client):
    # Login and get token
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )
    response = testing_client.post(
        "/login", data={"username": "testuser", "password": "TestPass123"}
    )
    token = response.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

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

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get("/accounts")
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

def test_get_account_by_account_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    # Query all existing accounts
    response_all = testing_client.get('/accounts')
    assert response_all.status_code == 200

    # Parse the JSON response
    accounts = json.loads(response_all.data)
    
    # Ensure there are accounts in the response
    assert len(accounts) > 0

    # Get the first account
    first_account = accounts['accounts'][0]
    
    # Perform assertions on the first account
    assert 'id' in first_account
    assert 'account_number' in first_account
    assert 'name' in first_account
    assert 'currency' in first_account
    assert 'country' in first_account

    # Now we can test get by account number
    response_single = testing_client.get('/accounts/' + str(first_account['id']))
    assert response_single.status_code == 200

# test update/put to the by default account id=1
def test_put_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is updated (PUT)
    THEN check the response is valid
    """
    response = testing_client.put('/accounts/1', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200

# test_delete_account would delete the by default created account with id=1
def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is deleted (DELETE)
    THEN check the response is valid
    """
    response = testing_client.delete('/accounts/1')
    assert response.status_code == 200