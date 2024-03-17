import traceback
from functools import wraps
from flask import request, jsonify, session
from config import Config
from infrastructure.exceptions import ApiError


def middleware(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print(
          f'Name{f.__name__}\n|Args {str(*args)} |\n|kwds {str(**kwds)}')
        try:
            result = f(*args, **kwds)
            return result
        except ApiError as e:
            print(f"ERROR :: {traceback.format_exc()}\nINFO : {str(e.message)} : {e.code}")
            return jsonify({'message': e.message}), e.code
        except Exception as e:
            print(f"ERROR :: {traceback.format_exc()}\nINFO : {str(e)}")
            return jsonify({'error': 'Error Interno'}), 500
    return wrapper