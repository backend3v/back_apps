from flask import Flask,jsonify,request
import base64,traceback
from aplication.api.routes.test import TestRoutes
from aplication.api.routes.traslate import TraslateRoutes
from infrastructure.storage_service import StorageService
from config import Config
from flask_cors import CORS
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

@app.route('/video',methods=['POST'])
def video():
    print('@???')
    name =request.json['name']
    print(name)
    result = StorageService().get_document(name)
    response = jsonify({"data":result}), 200
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

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