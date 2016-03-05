from flask import Flask
from server import config

app = Flask(__name__, template_folder='templates', static_folder='static',
            static_url_path='/static')
app.config.from_object(config)
