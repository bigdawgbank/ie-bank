import pytest

from iebank_api.models import Account


def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status, country , and created_at fields are defined correctly
    """
    account = Account("John Doe", "€", "Sweden")
    assert account.name == "John Doe"
    assert account.currency == "€"
    assert account.account_number is not None
    assert account.balance == 0.0
    assert account.status == "Active"
    assert account.country == "Sweden"


def test_create_bad_account():
    """
    GIVEN an Account model
    WHEN an account is created with invalid data
    THEN check that a ValueError is raised
    """
    # Test for None name
    with pytest.raises(ValueError) as excinfo:
        account = Account(None, "€", "Sweden")
    assert str(excinfo.value) == "Name cannot be empty."

    # Test for None currency
    with pytest.raises(ValueError) as excinfo:
        account = Account("John Doe", None, "Sweden")
    assert str(excinfo.value) == "Currency cannot be empty or None."

    # Test for empty country
    with pytest.raises(ValueError) as excinfo:
        account = Account("John Doe", "€", "")
    assert str(excinfo.value) == "Country cannot be empty."
