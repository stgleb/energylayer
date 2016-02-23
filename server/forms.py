from flask_wtf import Form
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
        if (self.email.data is None
            or self.password.data is None):
            return False

        # if user is None:
        #     self.email.errors = ('Unknown username')
        #     return False
        #
        # if not user.password != self.password.data:
        #     self.password.errors = ('Invalid password')
        #     return False
        user = User(email=self.email.data, password=self.password.data)
        self.user = user

        return True


class SignupForm(Form):
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
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True
