from flask.ext.login import current_user
from flask.ext.security import RegisterForm
from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import StringField
from wtforms import validators
from server.models import User


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])
    first_name = StringField('First Name', [])
    last_name = StringField('Last Name', [])


class EditForm(Form):
    username = StringField("Username",
                           [])
    firstname = StringField("First name",
                            [])
    lastname = StringField("Last name",
                           [])
    email = StringField("Email",
                        [validators.Email("Please enter your email address.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        return_value = True

        other_user = User.query.filter_by(email=self.email.
                                    data.lower()).first()

        if (current_user.id != other_user.id and
            other_user.email == current_user.email):
            self.email.errors = ("That email is already taken")
            return_value = False

        if (current_user.id != other_user.id and
            other_user.username == current_user.username):
            self.username.errors = ("That username is already taken")
            return_value = False

        return return_value