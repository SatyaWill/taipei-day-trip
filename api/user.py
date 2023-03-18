from flask import request, jsonify, make_response
from api import user
from controller import user_controller
from utils import token_required

controller = user_controller.UserController
# 註冊
@user.route("/api/user", methods=["POST"])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')
    return controller.signup(name, email, password, phone)

@user.route('/verify/<token>', methods=['GET'])
def signup_verify(token):
    return controller.signup_verify(token)

# 登入
@user.route("/api/user/auth", methods=["PUT"])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    return controller.signin(email, password)

# 取得登入資訊
@user.route("/api/user/auth", methods=["GET"])
def get_userinfo():
    try:
        if request.cookies:
            token = request.cookies.get("token")
            if token:
                return controller.get_userinfo(token)
        return {"data":None}, 200
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500

# 取得照片檔名
@user.route("/api/s3_url", methods=["GET"])
@token_required
def s3_url(user_email):
    return controller.s3_url(user_email)
            
# 修改頭貼
@user.route("/api/member_pic", methods=["PATCH"])
@token_required
def member_pic(user_email):
    member_pic = request.get_json()['member_pic']
    return controller.member_pic(user_email, member_pic)

# 修改名字
@user.route("/api/name", methods=["PATCH"])
@token_required
def edit_name(user_email):
    name = request.get_json()['name']
    return controller.edit_name(user_email, name)
        
# 修改電話
@user.route("/api/phone", methods=["PATCH"])
@token_required
def edit_phone(user_email):
    phone = request.get_json()['phone']
    return controller.edit_phone(user_email, phone)

# 修改密碼
@user.route("/api/password", methods=["PATCH"])
@token_required
def edit_password(user_email):
    old_password = request.get_json()['old_password']
    new_password = request.get_json()['new_password']
    return controller.edit_password(user_email, old_password, new_password)

# 取得帳號資訊
@user.route("/api/account", methods=["GET"])
@token_required
def get_account(user_email):
    return controller.get_account(user_email)

# 登出
@user.route("/api/user/auth", methods=["DELETE"])
def signout():
    res = make_response({"ok":True}, 200)
    res.set_cookie(key='token', value='', max_age=-1, httponly=True)
    return res

    
    



