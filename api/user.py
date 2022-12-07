from flask import Blueprint, request, jsonify, make_response
import sys, re
sys.path.append("..") 
from model import md5, selectone, edit_db, make_token, decode_token

user = Blueprint('user', __name__)
# 註冊
@user.route("/api/user", methods=["POST"])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    is_match = (re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$", email) and
                re.match("^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$", password))
    try:
        if is_match:
            res = selectone("SELECT COUNT(*) count FROM users WHERE email=%s", (email,))['count']
            if res == 1:
                return jsonify(error=True, message="e-mail 已註冊"), 400
            else:
                pw = md5(password)
                edit_db("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)", (name, email, pw))
                return {"ok":True}, 200
        else:
            return jsonify(error=True, message="電子信箱或密碼不符合要求"), 400
    except Exception as e:
        print(e)       
        return jsonify(error=True, message="伺服器內部錯誤"), 500

# 登入
@user.route("/api/user/auth", methods=["PUT"])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    print(email,password)
    pw = md5(password)
    res = selectone('SELECT id, name, email FROM users WHERE email=%s and password=%s',(email, pw))
    try:
        if res:
            resp = make_response({"ok":True}, 200)
            resp.set_cookie(key='token', value=make_token(res), max_age=60*60*24*7, httponly=True)
            return resp
        else:
            return jsonify(error=True, message="登入失敗，帳號或密碼錯誤"), 400
    except Exception as e:
        print(e)       
        return jsonify(error=True, message="伺服器內部錯誤"), 500

# 取得登入資訊
@user.route("/api/user/auth", methods=["GET"])
def get_userinfo():
    try:
        if request.cookies:
            token = request.cookies.get("token")
            res = decode_token(token)
            if res:
                del res['expire']
                return {"data":res}, 200
        else:
            return {"data":None}, 200
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500

# 登出
@user.route("/api/user/auth", methods=["DELETE"])
def signout():
#token=; Max-Age=-1
    res = make_response({"ok":True}, 200)
    res.set_cookie(key='token', value='', max_age=-1, httponly=True)
    return res

    
    



