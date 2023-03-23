
# Initiierung Flask Applikation

from flask import Flask

PRODUCTION_MODE = False
DEBUG_MODE = True
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
APP_SECRET_KEY = 'App Super Secret Key'

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['DEBUG'] = DEBUG_MODE
app.secret_key = APP_SECRET_KEY

import views
import apis
