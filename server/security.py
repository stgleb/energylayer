from flask.ext.security import RegisterForm, SQLAlchemyUserDatastore, Security
from flask.ext.security.forms import Required
from server.application import app
# Setup Flask-Security
from server.models import Role, db
from server.models import User
from wtforms import StringField

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])
    first_name = StringField('First Name', [])
    last_name = StringField('Last Name', [])



@app.before_first_request
def create_default_user():
    """
        Creates default user for newly deployed application
    :return:
    """
    db.create_all()
    admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_role = user_datastore.find_or_create_role(name='end-user', description='End user')
    # try yto find user in database
    default_admin = user_datastore.find_user(email='admin@admin.com')
    default_user = user_datastore.find_user(email='user@user.com')
    # create user
    if default_admin is None:
        default_admin = user_datastore.create_user(email='admin@admin.com', password="admin")
        user_datastore.add_role_to_user(default_admin, admin_role)
        user_datastore.add_role_to_user(default_admin, user_role)

    if default_user is None:
        default_user = user_datastore.create_user(email='user@user.com', password="1234")
        user_datastore.add_role_to_user(default_user, user_role)

    db.session.commit()

