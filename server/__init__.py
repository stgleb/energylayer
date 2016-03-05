from server import config
from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static',
            static_url_path='/static')

app.config.from_object(config)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
db.Session(expire_on_commit=False)

from server import controllers
# db.create_all()

