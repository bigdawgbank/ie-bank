import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
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
    logger.info("Running in UAT mode")
    app.config.from_object("config.GithubCIConfig")
else:
    logger.info("Running in production mode")
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)

from iebank_api.models import Account

with app.app_context():
    db.create_all()
    logger.info("Database tables created successfully")

CORS(app)

from iebank_api import routes
