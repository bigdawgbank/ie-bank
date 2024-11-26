import pytest
from iebank_api import app, db
from iebank_api.models import Account, User


@pytest.fixture(scope="function")
def app_context():
    with app.app_context():
        # Set up
        db.create_all()
        yield
        # Tear down
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def testing_client():
    with app.app_context():
        db.create_all()
        # user_id = 1
        # user_obj = db.session.get(User, user_id)
        # account = Account("Test Account", "€", "Argentina", user=user_obj)
        # db.session.add(account)
        # db.session.commit()
            # Register the user

    with app.test_client() as testing_client:
        with app.app_context():  # Ensure the app context is active
            yield testing_client

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope="module")
def register_and_authenticate(testing_client):

     # Register the user
    testing_client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )

    # Login to get token
    response = testing_client.post(
        "/login", data={"username": "testuser", "password": "TestPass123"}
    )
    token = response.json["token"]
    return token
