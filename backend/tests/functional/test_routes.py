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
