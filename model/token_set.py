from flask import request, jsonify
import jwt, sys, time, hashlib
from jwt import exceptions
from functools import wraps
sys.path.append("..") 
from setting import SECRET_KEY

def md5(pwd):  # 密碼加密
    SALT = b'2erer3asdfwerxdf34sdfsdfs90'
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
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(data):
    res = jwt.decode(data, SECRET_KEY, algorithms=["HS256"])
    return res

def token_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            if request.cookies:
                token = request.cookies.get("token")
                res = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_name = res['name']
                user_email = res['email']
            if not res:
                return jsonify(error=True, message="未登入系統，拒絕存取"), 403
        except exceptions.ExpiredSignatureError:
            msg = "(token失效)"
            return jsonify(error=True, message="未登入系統，拒絕存取"+msg), 403
        except jwt.DecodeError:
            msg = "(token認證失敗)"
            return jsonify(error=True, message="未登入系統，拒絕存取"+msg), 403
        except jwt.InvalidTokenError:
            msg = "(token無效)"
            return jsonify(error=True, message="未登入系統，拒絕存取"+msg), 403
        return f(user_name, user_email, *args, **kwargs), 200
    return wrapped

