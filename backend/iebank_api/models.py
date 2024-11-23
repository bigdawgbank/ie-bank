import random
import string
from datetime import datetime, timezone

from flask_login import UserMixin
from iebank_api import bcrypt, db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    country = db.Column(db.String(32), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def __repr__(self):
        return "<Event %r>" % self.account_number

    def __init__(self, name, currency, country, user=None):
        if not name:
            raise ValueError("Name cannot be empty.")
        self.name = name
        if currency is None or currency.strip() == "":
            raise ValueError("Currency cannot be empty or None.")
        self.currency = currency
        if not country:
            raise ValueError("Country cannot be empty.")
        self.country = country
        self.account_number = "".join(random.choices(string.digits, k=20))
        self.balance = 0.0
        self.status = "Active"
        if user:
            self.user_id = user.id


# TODO: Add fk here to the user that could be nullable to allow a user to manage accounts
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    accounts = db.relationship("Account", backref="owner", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def __init__(self, username, email, password):
        if not username:
            raise ValueError("Username cannot be empty")
        if not email:
            raise ValueError("Email cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def create_account(self, name, currency, country):
        """Helper method to create an account for this user"""
        account = Account(name, currency, country, self)
        db.session.add(account)
        return account

    def get_accounts(self):
        """Get all accounts owned by this user"""
        return self.accounts.all()
