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


class DevelopmentConfig(Config):
    if os.getenv("ENV") == "dev":
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
                dbuser=os.getenv("DBUSER"),
                dbpass=credential.get_token(
                    "https://ossrdbms-aad.database.windows.net"
                ).token,
                dbhost=os.getenv("DBHOST"),
                dbname=os.getenv("DBNAME"),
            )
        )
        DEBUG = True


class UATConfig(Config):
    if os.getenv("ENV") == "uat":
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
                dbuser=os.getenv("DBUSER"),
                dbpass=credential.get_token(
                    "https://ossrdbms-aad.database.windows.net"
                ).token,
                dbhost=os.getenv("DBHOST"),
                dbname=os.getenv("DBNAME"),
            )
        )
        DEBUG = True


class ProductionConfig(Config):
    if os.getenv("ENV") == "prod":
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
                dbuser=os.getenv("DBUSER"),
                dbpass=credential.get_token(
                    "https://ossrdbms-aad.database.windows.net"
                ).token,
                dbhost=os.getenv("DBHOST"),
                dbname=os.getenv("DBNAME"),
            )
        )
        DEBUG = True
