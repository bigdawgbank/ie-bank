def test_protected_route(testing_client):
    """Test accessing protected route with authenticated user"""
    # Register and login
    response = testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testPass123",
        },
    )
    print(response)
    response2 = testing_client.post(
        "/login", data={"username": "testuser", "password": "testPass123"}
    )
    print(response.status)

    # Test protected route
    response = testing_client.get("/accounts")
    assert response.status_code == 200


def test_login_failure(testing_client):
    """Test invalid login credentials"""
    response = testing_client.post(
        "/login", data={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_logout(testing_client):
    """Test logout functionality"""
    # Register and login first
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testPass123",
        },
    )
    testing_client.post(
        "/login", data={"username": "testuser", "password": "testPass123"}
    )

    # Test logout
    response = testing_client.post("/logout")
    assert response.status_code == 200

    # Verify can't access protected route after logout
    response = testing_client.get("/accounts")
    assert response.status_code == 401


def test_register_duplicate_user(testing_client):
    """Test registering duplicate user"""
    # Register first user
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testPass123",
        },
    )

    # Try to register same username
    response = testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "another@example.com",
            "password": "testPass123",
        },
    )
    assert response.status_code == 400


def test_authentication_required(testing_client):
    """Test authentication is required for protected routes"""
    response = testing_client.get("/accounts")
    assert response.status_code == 401
