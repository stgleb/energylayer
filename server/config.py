import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'super-secret'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/energylayer'
SQLALCHEMY_ECHO = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Flask-Security config
SECURITY_URL_PREFIX = ""
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/"
SECURITY_POST_LOGOUT_VIEW = "/login"
SECURITY_POST_REGISTER_VIEW = "/"
SECURITY_POST_CONFIRM_VIEW = '/'
SECURITY_CONFIRM_URL = '/confirm'
SECURITY_CHANGE_URL = '/reset'

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_TRACKABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

# EMAIL SETTINGS
MAIL_SERVER = 'mailtrap.io'
MAIL_PORT = 465
MAIL_USERNAME = '625646a9e3e2e44f'
MAIL_PASSWORD = 'a2ca2036ca900b'
MAIL_USE_TLS = True
MAIL_USE_SSL = False


# Oauth 2.0 settings
OAUTHLIB_INSECURE_TRANSPORT = "1"


# Pagination
PER_PAGE = 20
TOTAL_COUNT = 18
DEVICE_TIME_INTERVAL = 10

# Constants
VOLTAGE = "voltage"
POWER = "power"
TEMPERATURE = "temperature"
METRICS = (VOLTAGE, POWER, TEMPERATURE)
UNITS = {
    VOLTAGE: "v",
    POWER: "w",
    TEMPERATURE: "t"
}

GEO_IP_FILE = "GeoLite2-City.mmdb"
