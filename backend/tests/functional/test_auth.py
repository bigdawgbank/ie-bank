def test_protected_route(testing_client, register_and_authenticate):
    headers = {"Authorization": f"Bearer {register_and_authenticate}"}
    response = testing_client.get("/accounts", headers=headers)
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
