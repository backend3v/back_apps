import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY')
        self.host = os.getenv('HOST')
        self.port = os.getenv('PORT')
        self.debu = os.getenv('DEBUG')
        self.ttl_token = int(os.getenv('TTL'))