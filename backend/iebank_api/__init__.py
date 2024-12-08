import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from opencensus.ext.azure.log_exporter import AzureLogHandler  # Already imported
import logging  # <-- Added import for logging

load_dotenv()
app = Flask(__name__)

# -----------------------------------------------------
# NEW CODE ADDED HERE: Set up logger for Application Insights
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if connection_string:
    # If we have a connection string, send logs to Application Insights
    logger.addHandler(AzureLogHandler(connection_string=connection_string))
else:
    # Fallback: if no connection string, log to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
# -----------------------------------------------------

# Create extensions
db = SQLAlchemy()
jwt_manager = JWTManager()
bcrypt = Bcrypt()

# Your environment config loading stays the same
if os.getenv("ENV") == "local":
    logger.info("Running in local mode")
    app.config.from_object("config.LocalConfig")
elif os.getenv("ENV") == "dev":
    logger.info("Running in development mode")
    app.config.from_object("config.DevelopmentConfig")
elif os.getenv("ENV") == "ghci":
    logger.info("Running in GitHub mode")
    app.config.from_object("config.GithubCIConfig")
elif os.getenv("ENV") == "uat":
    logger.info("Running in UAT mode")
    app.config.from_object("config.GithubCIConfig")
else:
    logger.info("Running in production mode")
    app.config.from_object("config.ProductionConfig")

# Initialize extensions with app
db.init_app(app)
jwt_manager.init_app(app)
bcrypt.init_app(app)

# Import models
from iebank_api.models import Account, User

with app.app_context():
    db.create_all()
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@admin.com")
        admin_user = User.query.filter_by(email=admin_email).first()

        if not admin_user:
            print("Creating admin user...")
            admin_user = User(
                username="admin",
                email=admin_email,
                password=os.getenv("ADMIN_PASSWORD", "Password1234"),
                role="admin",
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.session.rollback()

CORS(app, supports_credentials=True)

from iebank_api import routes
