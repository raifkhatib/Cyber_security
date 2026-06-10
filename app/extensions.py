from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# Extensions are created once here and initialized by the app factory.
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
server_session = Session()
