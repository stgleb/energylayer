import os

from flask.ext.mail import Mail
from flask.ext.security import Security
from server import config
from server.forms import ExtendedRegisterForm
from flask.ext.login import LoginManager
from server.security import user_datastore
from server.application import app
from server.models import db

login_manager = LoginManager(app=app)

from server.controllers import *
from server.oauth.controllers import *

security = Security(app, user_datastore, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)
mail = Mail(app)


@security.context_processor
def security_context_processor():
    return dict(
        register_form=ExtendedRegisterForm
    )

app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

