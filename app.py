from flask import Flask,jsonify
import base64
from aplication.api.routes.test import TestRoutes
from aplication.api.routes.traslate import TraslateRoutes
from infrastructure.storage_service import StorageService
from config import Config
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World 33!'





@app.route('/videos')
def videos():
    return jsonify({"data":StorageService().get_documents()})

@app.route('/video')
def video():
    name = "English (auto-generated)] The Big Bang Theory _ Season 1 _ Episode 2 _ The Big Bran Hypothesis [DownSub.com].srt"
    result = StorageService().get_document(name)
    return jsonify({"data":result})

class Application:
    def __init__(self):
        #self.app = Flask(__name__,template_folder='aplication/templates')
        CORS(app)
        app.config['SECRET_KEY'] = Config().secret_key
        TraslateRoutes(app)
        TestRoutes(app)
def runner():
    app.run(host=Config().host, port=Config().port,
                    debug=Config().debu)

def run_app():
    aplication = Application()
    return aplication.app
if __name__ == '__main__':
    aplication = Application()
    aplication.runner()