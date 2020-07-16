from flask import Flask
from web.config import Config_KEY, Config_DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config_DB)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

from web import routes, models