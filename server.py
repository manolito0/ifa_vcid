#Methode um Unicorn zu Initialisieren
#Eigenentwicklung

from waitress import serve
from app.app import app

PRODUCTION_MODE = False
DEBUG_MODE = True
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
APP_SECRET_KEY = 'App Super Secret Key'

if __name__ == '__main__':
    if PRODUCTION_MODE:
        serve(app, host=SERVER_HOST, port=SERVER_PORT)
    else:
        app.run(threaded=True, host=SERVER_HOST, port=SERVER_PORT)
