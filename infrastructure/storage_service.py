import os
import firebase_admin
from firebase_admin import credentials, storage
import traceback,re,requests
from dotenv import load_dotenv
from infrastructure.singleton import SingletonMeta


class StorageService(metaclass=SingletonMeta):
    def __init__(self):
        self.app = None
        self.bucket = None
    def conect(self):
        
        try:
            project_folder = os.path.expanduser(os.getcwd())  # adjust as appropriate
            load_dotenv(os.path.join(project_folder, '.env'))
            print(f"----{os.getenv('CLIENT_ID')}")
            config = {
            "type": "service_account",
            "project_id": "englishapp-418617",
            "private_key_id": os.getenv('PRIVATE_KEY_ID'),
            "private_key": os.getenv('PRIVATE_KEY').replace(r'\n', '\n'),
            "client_email": "firebase-adminsdk-zn4f0@englishapp-418617.iam.gserviceaccount.com",
            "client_id": os.getenv('CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zn4f0%40englishapp-418617.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            }
            if self.app == None:
                cred = credentials.Certificate(config)
                self.app = firebase_admin.initialize_app(cred,{'storageBucket': 'englishapp-418617.appspot.com'})# fetch all the files in the bucket
                self.bucket = firebase_admin.storage.bucket()
                print(f"Name Bucket {list(self.bucket.list_blobs())}")
            return self.bucket
        except:
            print(traceback.format_exc())
            return None
    
    def get_documents(self):
        bucket = self.conect()
        items = list(bucket.list_blobs())
        new_data = []
        for i in items:
            new_data.append(str(i.name))
        return new_data
    
    def get_document(self,doc):
        print("ddd ",doc)
        bucket = self.conect()
        source_blob_name = doc
        if source_blob_name == None:
            return None
        blob = bucket.blob(source_blob_name)
        r = requests.get(f'https://firebasestorage.googleapis.com/v0/b/englishapp-418617.appspot.com/o/{doc}?alt=media&token=41ebb839-beff-4104-bd6c-d73aec6fdb64')
        content = r.content.decode()
        #print("ddd ",content)
        # path = str(os.getcwd())+"/temp.txt"
        # content = None
        # blob.download_to_filename(path)
        # with open(path) as file:
        #     content = file.read()
        dict_result = {}
        def to_ms(tiempo):
            hours = int(tiempo[0]) * 3600000
            minutes = int(tiempo[1]) * 60000
            seconds = int(tiempo[2]) * 1000
            miliseconds = seconds + minutes + hours
            miliseconds += int(tiempo[2]) % 1000
            miliseconds += int(tiempo[3])
            return miliseconds
        def process_match(obj_match):
            obj = obj_match[0].split(sep="\n")
            #print(obj)
            time = obj[1].split(sep=" --> ")
            #print(time)
            time = time[1].replace(",",":")
            time = time.split(":")
            #print(time)
            new_list = []
            for i in time:
                new_list.append(str(int(i)))
            time = ":".join(new_list)
            time = to_ms(new_list)
            dict_obj ={"end":time,"data":obj[2]}
            dict_result[obj[0]] = dict_obj
            return str(obj)
            
        patron = r'([0-9]{1,3}\n[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]\s-->\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]\n[\w\s]*?[^\n]*)'
        result = re.sub(patron, process_match,content)
        return dict_result
