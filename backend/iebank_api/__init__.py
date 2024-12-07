import os
<<<<<<< HEAD
import logging
=======
>>>>>>> 67baa060467d9012f1e228ab482c20ba9d572dc2
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from opencensus.ext.azure.log_exporter import AzureLogHandler

load_dotenv()
app = Flask(__name__)

# Create extensions first
db = SQLAlchemy()
jwt_manager = JWTManager()
bcrypt = Bcrypt()

<<<<<<< HEAD
# Logger setup for Application Insights
logger = logging.getLogger("iebank_logger")
logger.setLevel(logging.INFO)  # Adjust log level as needed

# Configure Azure Log Handler
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    handler = AzureLogHandler(connection_string=connection_string)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

# Select environment based on the ENV environment variable
=======

# Your environment config loading stays the same
>>>>>>> 67baa060467d9012f1e228ab482c20ba9d572dc2
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

# Create tables and initialize admin in a single context
with app.app_context():
    db.create_all()

    try:
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
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.session.rollback()

<<<<<<< HEAD

from iebank_api.models import Account, User

with app.app_context():
    db.create_all()
    logger.info("Database tables created successfully")

CORS(app)

=======
CORS(app, supports_credentials=True)
>>>>>>> 67baa060467d9012f1e228ab482c20ba9d572dc2
from iebank_api import routes
