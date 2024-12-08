import random
import string
from datetime import datetime, timezone
from enum import Enum
import os
import json

from sqlalchemy import Enum as SQLAlchemyEnum

from iebank_api import bcrypt, db


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


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

    def __init__(self, name, currency, country, user=None, balance=0.0):
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
        self.balance = balance
        self.status = "Active"
        if user:
            self.user_id = user.id

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.balance += amount


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(SQLAlchemyEnum(Role), nullable=False, default=Role.USER)
    accounts = db.relationship(
        "Account", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self, username, email, password, role="user"):
        # Validate username
        if not username or username.strip() == "":
            raise ValueError("Username cannot be empty")

        # Validate email
        if not email:
            raise ValueError("Email cannot be empty")

        # Validate password
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain a number")

        # Check for duplicate email
        if db.session.query(User).filter_by(email=email).first():
            raise ValueError("Email already registered")

        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        """Set hashed password."""
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain a number")

        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Check password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def create_account(self, name, currency, country):
        """Helper method to create an account for this user"""
        account = Account(name, currency, country, self)
        db.session.add(account)
        return account

    def get_accounts(self):
        """Get all accounts owned by this user"""
        return self.accounts.all()


class BankTransfer:
    def __init__(self, from_account, to_account, amount):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def process_transfer(self):
        transfer_success = False

        
        if self.from_account.balance < self.amount:
            return transfer_success
        
        exchange_rate_obj = ExchangeRate()
        exchange_rate_value = exchange_rate_obj.get_exchange_rate(
            self.from_account.currency, self.to_account.currency
        )
        converted_amount = self.amount * exchange_rate_value

        self.from_account.withdraw(self.amount)
        self.to_account.deposit(converted_amount)
        db.session.commit()
        transfer_success = True
        return transfer_success


class ExchangeRate:
    def get_exchange_rate(self, from_currency, to_currency):
        if from_currency == to_currency:
            return 1
        
        # Load the JSON configuration file
        with open('currency_exchange_config.json') as config_file:
            config = json.load(config_file)

        # Translate between currency symbols to words
        currency_symbol_to_word = {
            '€': 'EURO',
            '$': 'USD',
        }

        # Get the currency words
        from_currency_word = currency_symbol_to_word[from_currency]
        to_currency_word = currency_symbol_to_word[to_currency]
        
        # Get the exchange rate from the config file
        exchange_rate_name = f"{from_currency_word}_TO_{to_currency_word}_EXCHANGE_RATE"
        if exchange_rate_name in config['exchange_rate']:
            exchange_rate = float(config['exchange_rate'][exchange_rate_name])
        else:
            # Calculate the reverse exchange rate
            reverse_exchange_rate_name = f"{to_currency_word}_TO_{from_currency_word}_EXCHANGE_RATE"
            reverse_exchange_rate = float(config['exchange_rate'][reverse_exchange_rate_name])
            exchange_rate = round(1 / reverse_exchange_rate, 2)

        return exchange_rate
        