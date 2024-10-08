import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    DEBUG = True


class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    DEBUG = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:"
        f"{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
    )
    DEBUG = True
