import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from opencensus.ext.azure.log_exporter import AzureLogHandler

app = Flask(__name__)

load_dotenv()

# Logger setup for Application Insights
logger = logging.getLogger("iebank_logger")
logger.setLevel(logging.INFO)  # Adjust log level as needed

# Configure Azure Log Handler
connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")
if connection_string:
    handler = AzureLogHandler(connection_string=connection_string)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

# Select environment based on the ENV environment variable
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
<<<<<<< HEAD
    logger.info("Running in UAT mode")
    app.config.from_object("config.GithubCIConfig")
=======
    print("Running in uat mode")
    app.config.from_object("config.UATConfig")
>>>>>>> origin/main
else:
    logger.info("Running in production mode")
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)
jwt_manager = JWTManager(app)
bcrypt = Bcrypt(app)


def create_admin_user():
    """Create admin user if it doesn't exist"""
    # Check if admin user exists
    admin_user = User.query.filter_by(
        email=os.getenv("ADMIN_EMAIL", "admin@admin.com")
    ).first()

    if not admin_user:
        print("Creating admin user...")

        admin_user = User(
            username="admin",
            email=os.getenv("ADMIN_EMAIL", "admin@admin.com"),
            password=os.getenv("ADMIN_PASSWORD", "Password1234"),
            role="admin",
        )

        try:
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")
            db.session.rollback()
    else:
        print("Admin user already exists")


from iebank_api.models import Account, User

with app.app_context():
    db.create_all()
<<<<<<< HEAD
    logger.info("Database tables created successfully")

CORS(app)
=======
    create_admin_user()
CORS(app, supports_credentials=True)
>>>>>>> origin/main

from iebank_api import routes
