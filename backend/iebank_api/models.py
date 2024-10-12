import random
import string
from datetime import datetime

from iebank_api import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    country = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Event %r>" % self.account_number

    # Have value checks for application
    def __init__(self, name, currency, country):
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
