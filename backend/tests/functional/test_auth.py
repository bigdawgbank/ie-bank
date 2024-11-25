def test_protected_route(testing_client):
    # Register and login to get token
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testPass123",
        },
    )
    response = testing_client.post(
        "/login", data={"username": "testuser", "password": "testPass123"}
    )
    token = response.json["token"]

    # Test protected route with token
    response = testing_client.get(
        "/accounts", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_authentication_required(testing_client):
    response = testing_client.get("/accounts")
    assert response.status_code == 401


def test_login_failure(testing_client):
    response = testing_client.post(
        "/login", data={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_register_duplicate_user(testing_client):
    # First registration
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testPass123",
        },
    )

    # Duplicate registration
    response = testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "another@example.com",
            "password": "testPass123",
        },
    )
    assert response.status_code == 500
