from flask.ext.mail import Mail
from flask.ext.security import Security
from server import config
from flask.ext.login import LoginManager
from server.security import ExtendedRegisterForm, user_datastore
from server.application import app
from server.models import db
from flask_bootstrap import Bootstrap

login_manager = LoginManager(app=app)

from server import controllers

security = Security(app, user_datastore, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)
mail = Mail(app)
Bootstrap(app)


@security.context_processor
def security_context_processor():
    return dict(
        register_form=ExtendedRegisterForm
    )
