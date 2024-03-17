from flask import Flask

from aplication.api.routes.test import TestRoutes
from aplication.api.routes.traslate import TraslateRoutes
from config import Config
from flask_cors import CORS


app = Flask(__name__,template_folder='aplication/templates')
class Application:
    def __init__(self):
        #self.app = Flask(__name__,template_folder='aplication/templates')
        CORS(app)
        app.config['SECRET_KEY'] = Config().secret_key
        TraslateRoutes(app)
        TestRoutes(app)
    def runner(self):
        app.run(host=Config().host, port=Config().port,
                     debug=Config().debu)

def run_app():
    aplication = Application()
    return aplication.app
if __name__ == '__main__':
    aplication = Application()
    aplication.runner()