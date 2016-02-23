from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static',
            static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from server import controllers
login_manager.login_view = 'login'
db.create_all()

