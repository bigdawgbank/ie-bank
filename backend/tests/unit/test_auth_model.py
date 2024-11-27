import pytest

from iebank_api import app, db
from iebank_api.models import User


def test_create_user(app_context):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password hash, and username fields are defined correctly
    """
    user = User(email="test@test.com", username="Test User", password="Password123")
    assert user.email == "test@test.com"
    assert user.username == "Test User"
    assert user.password_hash is not None
    assert user.password_hash != "Password123"
    assert user.check_password("Password123")
    assert not user.check_password("wrong_password")


def test_create_bad_user(app_context):
    """
    GIVEN a User model
    WHEN a user is created with invalid data
    THEN check that a ValueError is raised
    """
    # Test for None email
    with pytest.raises(ValueError) as excinfo:
        user = User(username="Test User", email=None, password="Password123")
    assert str(excinfo.value) == "Email cannot be empty"

    # Test for empty email
    with pytest.raises(ValueError) as excinfo:
        user = User(username="Test User", email="", password="Password123")
    assert str(excinfo.value) == "Email cannot be empty"

    # Test for empty username
    with pytest.raises(ValueError) as excinfo:
        user = User(username="", email="test@test.com", password="Password123")
    assert str(excinfo.value) == "Username cannot be empty"


def test_password_validation(app_context):
    """
    GIVEN a User instance
    WHEN setting a password
    THEN check password validation rules
    """
    # Test empty password
    with pytest.raises(ValueError) as excinfo:
        user = User(username="Test User", email="test@test.com", password="")
    assert "Password cannot be empty" in str(excinfo.value)

    # Test short password
    with pytest.raises(ValueError) as excinfo:
        user = User(username="Test User", email="test@test.com", password="short")
    assert "Password must be at least 8 characters" in str(excinfo.value)

    # Test valid password
    user = User(username="Test User", email="test@test.com", password="ValidPass123")
    assert user.check_password("ValidPass123")


def test_user_unique_email(app_context):
    """
    GIVEN a User model
    WHEN two users are created with the same email
    THEN check that an error is raised
    """
    # Create first user
    user1 = User(username="Test User 1", email="test@test.com", password="Password123")
    db.session.add(user1)
    db.session.commit()

    # Try to create second user with same email
    with pytest.raises(ValueError) as excinfo:
        user2 = User(
            username="Test User 2", email="test@test.com", password="Password123"
        )
    assert str(excinfo.value) == "Email already registered"
