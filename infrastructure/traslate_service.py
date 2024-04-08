import os
import firebase_admin
from firebase_admin import credentials, storage
import traceback,re,requests
from dotenv import load_dotenv
from infrastructure.singleton import SingletonMeta
from deep_translator import GoogleTranslator

class TraslateService(metaclass=SingletonMeta):
    def __init__(self):
        self.app = None
    def get_traslate(self,phrase):
        traductor = GoogleTranslator(source='en', target='es')
        resultado = traductor.translate(str(phrase))
        return resultado
