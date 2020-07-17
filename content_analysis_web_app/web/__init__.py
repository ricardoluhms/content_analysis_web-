from flask import Flask
from web.config import Config_KEY, Config_DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

### Starts the app
app = Flask(__name__)
app.config.from_object(Config_DB)

### Starts the Database
db = SQLAlchemy(app)

### To be detailed
migrate = Migrate(app, db)

### To be detailed
login_manager = LoginManager(app)

from web import routes, models