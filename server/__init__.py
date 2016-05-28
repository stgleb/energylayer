import os
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.security import Security
from server import config
from server.application import app
from server.forms import ExtendedRegisterForm
from server.persistence.models import db
from server.security import user_datastore
from flask_admin import helpers

login_manager = LoginManager(app=app)

from server.controllers import *
from server.api import *
from server.oauth.controllers import *
from server.admin import *
from server.utils import *

security = Security(app, user_datastore, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)
mail = Mail(app)


@security.context_processor
def security_context_processor():
    return dict(
        register_form=ExtendedRegisterForm,
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
    )

app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

