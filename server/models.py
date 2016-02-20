import argparse

import time

from server import app
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), unique=True)
    registration_date = db.Column(db.Integer)
    devices = db.relationship('Device', backref='person',
                              lazy='dynamic')

    def __init__(self, user_name, email, first_name="", last_name=""):
        self.user_name = user_name
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = int(time.time())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "User %s %d".format(self.user_name, self.id)


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, uuid, user_id):
        self.uuid = uuid
        self.user_id = user_id


class Metrics(db.Model):
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
    main()
