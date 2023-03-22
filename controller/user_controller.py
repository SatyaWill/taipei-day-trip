from flask import jsonify, make_response
from model import user_model, generate_upload_url
from utils import md5, make_token, decode_token, validate, send_verification_email
from setting import REDIS_HOST
import uuid, json, redis, logging
logger = logging.getLogger(__name__)
model = user_model.UserModel
Redis = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

class UserController:
    @staticmethod
    def signup(name, email, password, phone):
        errors = validate.signup_data(name, email, password, phone)
        if errors:
            return jsonify({"error": True, "message": errors}), 400
        elif model.signup(email):
            return jsonify({"error": True, "message": "email已註冊過"}), 400
        else:
            try:
                token = str(uuid.uuid4())
                user_data = {
                    'name': name,
                    'email': email,
                    'password': md5(password),
                    'phone': phone,
                }
                Redis.set(token, json.dumps(user_data), ex=1800)
                send_verification_email(name, email, token)
                return {"ok": True}, 200
            except Exception as e:
                logger.error("err_signup_c(%s):%s", email, e)
                return {"error": True, "message": "伺服器內部錯誤"}, 500
            
    @staticmethod
    def signup_verify(token):
        try:
            user_data_str = Redis.get(token)
            if not user_data_str:
                return jsonify({"error": True, "message": "驗證連結失效或錯誤"}), 400
            user_data = json.loads(user_data_str)
            res = model.signup_verify(user_data)
            if res:
                Redis.delete(token)
                return {"ok": True}, 200   
            else:
                return jsonify({"error": True, "message": "email已註冊"}), 400
        except Exception as e:
            logger.error("err_signup_verify_c:%s", e)
            return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
            
    @staticmethod
    def signin(email, password):
        res = model.signin(email, password)
        try:
            if res:
                resp = make_response({"ok":True}, 200)
                resp.set_cookie(key='token', value=make_token(res), max_age=60*60*24*7, httponly=True)
                return resp
            else:
                return jsonify(error=True, message="登入失敗，帳號或密碼錯誤"), 400
        except Exception as e:
            logger.error("err_signup_verify_c(%s):%s", email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500
    
    @staticmethod
    def get_userinfo(token):
        try:
            user_id = decode_token(token)['id']
            user_info = model.get_userinfo(user_id)
            if user_info:
                return {"data": user_info}, 200
            return {"data":None}, 200        
        except Exception as e:
            logger.error("err_get_userinfo_c:%s", e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500
    
    @staticmethod
    def s3_url(user_email):
        if user_email:
            return generate_upload_url(), 200
        
    @staticmethod
    def member_pic(user_email, member_pic):
        try:
            res = model.member_pic(user_email, member_pic)
            if res:          
                return {"ok":True}, 200
            else:
                return jsonify(error=True, message="資料未更新"), 400
        except Exception as e:
            logger.error("err_member_pic_c(%s):%s", user_email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500
        
    @staticmethod
    def edit_name(user_email, name):
        try:
            if not name:
                return jsonify(error=True, message="姓名未填寫"), 400
            else:
                res = model.edit_name(user_email, name)
                if res:          
                    return {"ok":True}, 200
                else:
                    return jsonify(error=True, message="資料未更新"), 400
        except Exception as e:
            logger.error("err_edit_name_c(%s):%s", user_email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500

    @staticmethod
    def edit_phone(user_email, phone):
        if not validate.phone(phone):
            return jsonify(error=True, message="格式不符"), 400
        try:
            res = model.edit_phone(user_email, phone)
            if res:          
                return {"ok":True}, 200
            else:
                return jsonify(error=True, message="資料未更新"), 400
        except Exception as e:
            logger.error("err_edit_phone_c(%s):%s", user_email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500
            
    @staticmethod
    def edit_password(user_email, old_password, new_password):
        if not old_password or not new_password:
            return jsonify(error=True, message="請輸入舊密碼和新密碼"), 400
        elif old_password == new_password:
            return jsonify(error=True, message="新密碼不能和舊密碼相同"), 400
        elif not validate.password(new_password):
            return jsonify(error=True, message="新密碼格式不符"), 400
        try:
            res = model.edit_password(user_email, old_password, new_password)
            if res:          
                return {"ok":True}, 200
            else:
                return jsonify(error=True, message="密碼輸入錯誤"), 400
        except Exception as e:
            logger.error("err_edit_password_c(%s):%s", user_email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500
        
        
    @staticmethod
    def get_account(user_email):
        try:
            res = model.get_account(user_email)     
            return {"data":res}, 200
        except Exception as e:
            logger.error("err_get_account_c(%s):%s", user_email, e) 
            return jsonify(error=True, message="伺服器內部錯誤"), 500

