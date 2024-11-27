import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()

# Select environment based on the ENV environment variable
if os.getenv("ENV") == "local":
    print("Running in local mode")
    app.config.from_object("config.LocalConfig")
elif os.getenv("ENV") == "dev":
    print("Running in development mode")
    app.config.from_object("config.DevelopmentConfig")
elif os.getenv("ENV") == "ghci":
    print("Running in github mode")
    app.config.from_object("config.GithubCIConfig")
elif os.getenv("ENV") == "uat":
    print("Running in uat mode")
    app.config.from_object("config.UATConfig")
else:
    print("Running in production mode")
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)
jwt_manager = JWTManager(app)
bcrypt = Bcrypt(app)


from iebank_api.models import Account, User

with app.app_context():
    db.create_all()
CORS(app, supports_credentials=True)

from iebank_api import routes
