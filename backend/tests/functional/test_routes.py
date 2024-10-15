import pytest

from iebank_api import app


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


def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "currency": "€", "country": "Sweden"}
    )
    assert response.status_code == 201


# Custom test
def test_create_bad_account(testing_client):
    """
    GIVEN a Flask application
    WHEN an account is created with invalid data
    THEN check that the response status code is 400
    """

    response = testing_client.post(
        "/accounts", json={"currency": "€", "country": "Sweden"}
    )
    assert response.status_code == 400
    assert response.json.get("error") == "Name cannot be empty."

    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "currency": None, "country": "Sweden"}
    )
    assert response.status_code == 400
    assert response.json.get("error") == "Currency cannot be empty or None."

    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "currency": "€", "country": ""}
    )
    assert response.status_code == 400
    assert response.json.get("error") == "Country cannot be empty."
