import pytest

from iebank_api import app, db
from iebank_api.models import Account


@pytest.fixture(scope="function")
def app_context():
    with app.app_context():
        # Set up
        db.create_all()
        yield
        # Tear down
        db.session.remove()
        db.drop_all()


@pytest.fixture
def testing_client(scope="module"):
    with app.app_context():
        db.create_all()
        account = Account("Test Account", "€", "Africa")
        db.session.add(account)
        db.session.commit()

    with app.test_client() as testing_client:
        with app.app_context():  # Ensure the app context is active
            yield testing_client

    with app.app_context():
        db.drop_all()
