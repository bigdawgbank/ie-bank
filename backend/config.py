import os

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    DEBUG = True


class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    DEBUG = True


# Use for both uat and dev
class DevelopmentConfig(Config):
    if os.getenv("ENV") == "dev":
        # Initialize Azure Credential
        credential = DefaultAzureCredential()

        # Retrieve the access token for Azure Database for PostgreSQL
        token = credential.get_token("https://ossrdbms-aad.database.windows.net").token

        # Update the SQLALCHEMY_DATABASE_URI for Azure AD authentication
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}@{dbhost}:{dbport}/{dbname}?sslmode=require".format(
                dbuser=os.getenv("DBUSER"),
                dbhost=os.getenv("DBHOST"),
                dbport=os.getenv("DBPORT", "5432"),  # Default to port 5432
                dbname=os.getenv("DBNAME"),
            )
        )

        # Pass the token as a connection argument
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"password": token}}
        DEBUG = True


# Added custom config
class UATConfig(Config):
    if os.getenv("ENV") == "uat":
        # Initialize Azure Credential
        credential = DefaultAzureCredential()

        # Retrieve the access token for Azure Database for PostgreSQL
        token = credential.get_token("https://ossrdbms-aad.database.windows.net").token

        # Update the SQLALCHEMY_DATABASE_URI for Azure AD authentication
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}@{dbhost}:{dbport}/{dbname}?sslmode=require".format(
                dbuser=os.getenv("DBUSER"),
                dbhost=os.getenv("DBHOST"),
                dbport=os.getenv("DBPORT", "5432"),  # Default to port 5432
                dbname=os.getenv("DBNAME"),
            )
        )

        # Pass the token as a connection argument
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"password": token}}
        DEBUG = True


class ProductionConfig(Config):
    if os.getenv("ENV") == "uat":
        # Initialize Azure Credential
        credential = DefaultAzureCredential()

        # Retrieve the access token for Azure Database for PostgreSQL
        token = credential.get_token("https://ossrdbms-aad.database.windows.net").token

        # Update the SQLALCHEMY_DATABASE_URI for Azure AD authentication
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}@{dbhost}:{dbport}/{dbname}?sslmode=require".format(
                dbuser=os.getenv("DBUSER"),
                dbhost=os.getenv("DBHOST"),
                dbport=os.getenv("DBPORT", "5432"),  # Default to port 5432
                dbname=os.getenv("DBNAME"),
            )
        )

        # Pass the token as a connection argument
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"password": token}}
        DEBUG = True
