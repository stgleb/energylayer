import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'super-secret'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
