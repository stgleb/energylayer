from flask_wtf import Form
from server.utils import compare_password, hash_password
from wtforms import StringField, BooleanField
from wtforms import PasswordField
from wtforms import validators
from server.models import User


class LoginForm(Form):
    email = StringField('email', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', [validators.Optional()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        return_value = True
        user = User.query.filter_by(email=self.email.data).first()

        # Check if all required fields are there
        if user is None:
            self.email.errors = ('Email not found')
            return_value = False

        if self.password.data is None:
            self.password.errors = ('Invalid password')
            return_value = False

        if user and not compare_password(user, self.password.data):
            self.password.errors = ('Wrong password')
            return_value = False

        self.user = user

        return return_value


class SignupForm(Form):
    username = StringField("Username",
                           [validators.DataRequired("Please enter your username name.")])
    firstname = StringField("First name",
                            [validators.DataRequired("Please enter your first name.")])
    lastname = StringField("Last name",
                           [validators.DataRequired("Please enter your last name.")])
    email = StringField("Email",
                        [validators.DataRequired("Please enter your email address."),
                         validators.Email("Please enter your email address.")])
    password = PasswordField('Password',
                             [validators.DataRequired("Please enter a password.")])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        return_value = True

        user = User.query.filter_by(email=self.email.
                                    data.lower()).first()
        if user:
            self.email.errors = ("That email is already taken")
            return_value = False

        if not self.lastname.data:
            self.lastname.errors = ("Enter last name")
            return_value = False

        if not self.firstname.data:
            self.firstname.errors = ("Enter first name")
            return_value = False

        if not self.username.data:
            self.username.errors = ("Enter username")
            return_value = False

        if not self.password.data:
            self.password.errors = ("Empty password is not allowed")
            return_value = False

        return return_value