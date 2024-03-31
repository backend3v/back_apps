from flask import Flask,jsonify
import base64
from aplication.api.routes.test import TestRoutes
from aplication.api.routes.traslate import TraslateRoutes
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
    try:

        config = {
  "type": "service_account",
  "project_id": "englishapp-418617",
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY'),
  "client_email": "firebase-adminsdk-zn4f0@englishapp-418617.iam.gserviceaccount.com",
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zn4f0%40englishapp-418617.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
        cred = credentials.Certificate(config)
        app = firebase_admin.initialize_app(cred,{'storageBucket': 'englishapp-418617.appspot.com'})# fetch all the files in the bucket
    except:
        pass
    #list(bucket.list_blobs())
    items = list(firebase_admin.storage.bucket().list_blobs())
    new_data = []
    for i in items:
        new_data.append(str(i.name))
    print(f"Name Bucket {list(firebase_admin.storage.bucket().list_blobs())}")
    return jsonify({'data':new_data})


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