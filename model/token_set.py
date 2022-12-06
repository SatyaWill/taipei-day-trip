from flask import request, jsonify
import jwt, sys, hashlib, time
from jwt import exceptions
from functools import wraps
sys.path.append("..") 
from model.fetch import *

secret_key = "b'\xd6\x81\xdbd\xe0\xe1\xd9>\xbfs\x03\x19\xab?\xa5\x9f\xf9o\xf5\xb4'"
SALT = b'2erer3asdfwerxdf34sdfsdfs90'
def md5(pwd):
    obj = hashlib.md5(SALT)
    obj.update(pwd.encode('utf-8'))
    return obj.hexdigest()

def make_token(data):
    payload = {
        "id": data['id'],
        "name": data['name'],
        "email": data['email'],
        "expire": int(time.time())+60*60*24*7
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            if request.cookies:
                token = request.cookies.get("token")
                res = jwt.decode(token, secret_key, algorithms=["HS256"])
                if res:
                    return 200
            else:
                return jsonify(error=True, message="未登入系統，拒絕存取"), 403
        except exceptions.ExpiredSignatureError:
            msg = "(token失效)"
        except jwt.DecodeError:
            msg = "(token認證失敗)"
        except jwt.InvalidTokenError:
            msg = "(token無效)"
        return f(*args, **kwargs), jsonify(error=True, message="未登入系統，拒絕存取"+msg), 403
    return wrapped

