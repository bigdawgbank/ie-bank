import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_DOMAIN = os.getenv("DOMAIN")
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    DEBUG = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
        dbuser=os.getenv("DBUSER"),
        dbpass=os.getenv("DBPASS"),
        dbhost=os.getenv("DBHOST"),
        dbname=os.getenv("DBNAME"),
    )
    DEBUG = True


class ProductionConfig(Config):
    pass
