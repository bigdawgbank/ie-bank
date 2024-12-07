import os
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

CORS(app, supports_credentials=True)
from iebank_api import routes
