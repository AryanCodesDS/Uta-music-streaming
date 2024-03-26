import os,secrets
class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = secrets.token_urlsafe()
    SECURITY_PASSWORD_SALT = secrets.SystemRandom().getrandbits(128)
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
    