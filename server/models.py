import argparse
import time

from flask import url_for
from hashlib import md5
from server.application import app
from flask.ext.security import UserMixin
from flask.ext.login import make_secure_token
from flask.ext.security import RoleMixin
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.Session(expire_on_commit=False)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    # TODO: add Oauth support with Flask-Social
    # social_id = db.Column(db.String(64), unique=True)
    # nickname = db.Column(db.String(64))
    email = db.Column(db.String(255), unique=True)
    registration_date = db.Column(db.Integer)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count = db.Column(db.Integer)
    avatar_image = db.Column(db.LargeBinary)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    devices = db.relationship('Device', backref='user',
                              lazy='dynamic')

    def get_auth_token(self):
        return make_secure_token(self.username)

    def get_id(self):
        return self.id

    @property
    def avatar(self, size=256):

        # If there is avatar in database use it
        # or use Gravatar instead
        if self.avatar_image:
            return url_for('get_avatar')
        image_url = 'http://www.gravatar.com/avatar/' + \
                    md5(self.email.encode('utf-8')).hexdigest() + \
                    '?d=mm&s=' + str(128)

        return image_url

    def __init__(self, email, password, username="", first_name="", last_name="", active=False, roles=[]):
        self.email = email
        self.password = password
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.roles = roles
        self.registration_date = int(time.time())

    def __repr__(self):
        return "{0}".format(self.first_name)


class Device(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip_addr = db.Column(db.String(40))
    measurements = db.relationship('Measurement', backref='device',
                                   lazy='dynamic')

    def __init__(self, uuid, ip_addr):
        self.uuid = uuid
        self.ip_addr = ip_addr


class Measurement(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    gpio = db.Column(db.Integer)
    voltage = db.Column(db.Integer)
    power = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def __init__(self, device_id, gpio, voltage, power, temperature):
        self.device_id = device_id
        self.gpio = gpio
        self.voltage = voltage
        self.power = power
        self.temperature = temperature
        self.timestamp = int(time.time())


def parse_args():
    parser = argparse.ArgumentParser(description='Command line arguments.')
    parser.add_argument("-c", type=str, dest="cmd",
                        help="command", default="create")
    return parser.parse_args()


def main():
    arg_obj = parse_args()

    if arg_obj.cmd == "drop":
        db.drop_all()
    elif arg_obj.cmd == "create":
        db.create_all()

if __name__ == '__main__':
    db.create_all()

