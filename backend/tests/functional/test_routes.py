def test_create_account(testing_client):
    """Test creating a new account"""
    # First register and login
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )

    testing_client.post(
        "/login", data={"username": "testuser", "password": "TestPass123"}
    )

    # Then create account
    response = testing_client.post(
        "/accounts",
        json={"name": "My Savings Account", "currency": "€", "country": "Ireland"},
    )

    # Verify response
    assert response.status_code == 201
    assert response.json["name"] == "My Savings Account"
    assert response.json["currency"] == "€"
    assert response.json["country"] == "Ireland"
    assert "account_number" in response.json
    assert "user_id" in response.json

    # Verify account appears in user's accounts
    accounts_response = testing_client.get("/accounts")
    assert accounts_response.status_code == 200
    # Check if response is wrapped in 'accounts' key
    accounts = accounts_response.json.get("accounts", accounts_response.json)
    assert len(accounts) == 1
    assert accounts[0]["name"] == "My Savings Account"


# Test invalid requests
def test_create_account_invalid_data(testing_client):
    """Test creating account with invalid data"""
    # Login first
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )
    testing_client.post(
        "/login", data={"username": "testuser", "password": "TestPass123"}
    )

    # Test missing name
    response = testing_client.post(
        "/accounts", json={"currency": "€", "country": "Ireland"}
    )
    assert response.status_code == 400
    assert "error" in response.json

    # Test missing currency
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "country": "Ireland"}
    )
    assert response.status_code == 400
    assert "error" in response.json

    # Test missing country
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "currency": "€"}
    )
    assert response.status_code == 400
    assert "error" in response.json


def test_create_account_unauthorized(testing_client):
    """Test creating account without logging in"""
    response = testing_client.post(
        "/accounts", json={"name": "My Account", "currency": "€", "country": "Ireland"}
    )
    assert response.status_code == 401  # or 403 depending on your setup
