## main.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from recycle_marketplace.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from recycle_marketplace import models, views
