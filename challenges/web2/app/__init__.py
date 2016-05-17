from flask import Flask
from flask_sqlalchemy import SQLAlchemy

key = 'w0wM0R3M0kep0n'
hostname = 'localhost:5000'

class ConfigClass(object):
    # Flask settings
    SECRET_KEY                      = 'THIS IS AN INSECURE SECRET'
    SQLALCHEMY_DATABASE_URI         = 'sqlite:///basic_app.sqlite'
    SQLALCHEMY_ECHO                 = True
    USER_ENABLE_EMAIL               = False
    USER_ENABLE_CONFIRM_EMAIL       = False
    USER_ENABLE_FORGOT_PASSWORD     = False
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM = True
    USER_AUTO_LOGIN                  = True
    USER_AUTO_LOGIN_AFTER_CONFIRM    = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_REGISTER   = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = USER_AUTO_LOGIN
    USER_PASSWORD_HASH_MODE = 'plaintext'

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

# Initialize Flask extensions
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy

from app import main
main.app_init()

from app import models
from app import views

