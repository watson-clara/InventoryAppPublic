from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
