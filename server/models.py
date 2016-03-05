import argparse
import time

from flask.ext.login import UserMixin
from flask.ext.login import make_secure_token
from flask.ext.security import RoleMixin
from server import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    # social_id = db.Column(db.String(64), nullable=False, unique=True)
    # nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True)
    registration_date = db.Column(db.Integer)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    devices = db.relationship('Device', backref='person',
                              lazy='dynamic')

    def get_auth_token(self):
        return make_secure_token(self.username)

    def get_id(self):
        return self.id

    def __init__(self, email, password, username="", first_name="", last_name=""):
        self.email = email
        self.password = password
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = int(time.time())

    def __repr__(self):
        return "{0}".format(self.first_name)


class Device(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, uuid, user_id):
        self.uuid = uuid
        self.user_id = user_id


class Metrics(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    time_stamp = db.Column(db.Integer)
    measurement = db.Column(db.Float)


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

