from .db import pool, selectone, edit_db
from .s3 import delete_pic
from utils import md5
import logging
logger = logging.getLogger(__name__)

class UserModel:
    @staticmethod
    def signup(email):
        try:
            with pool.get_connection() as db:
                return selectone(db, "SELECT COUNT(*) count FROM users WHERE email=%s", (email,))['count']
        except Exception as e:
            logger.error("err_signup(%s):%s", email, e)
        
    @staticmethod
    def signup_verify(d):
        try:
            with pool.get_connection() as db:
                sql = "INSERT INTO users(name, email, phone, password) VALUES (%s, %s, %s, %s)"
                return edit_db(db, sql, (d['name'], d['email'], d['phone'], d['password']))
        except Exception as e:
            logger.error("err_signup_verify:%s", e)
            return False
        
    @staticmethod
    def signin(email, password):
        try:
            with pool.get_connection() as db:
                sql = 'SELECT id, name, email FROM users WHERE email=%s and password=%s'
                return selectone(db, sql,(email, md5(password)))
        except Exception as e:
            logger.error("err_signin(%s):%s", email, e)
        
    @staticmethod
    def get_userinfo(user_id):
        try:
            with pool.get_connection() as db:
                sql = 'SELECT id, name, email, member_pic FROM users WHERE id=%s'
                return selectone(db, sql, (user_id,))
        except Exception as e:
            logger.error("err_get_userinfo(%s):%s", user_id, e)
    
    @staticmethod
    def member_pic(user_email, member_pic):
        try:
            with pool.get_connection() as db:
                if member_pic == "":
                    sql = 'SELECT member_pic FROM users WHERE email=%s'
                    r = selectone(db, sql, (user_email,))
                    delete_pic(r['member_pic'])
                    return edit_db('UPDATE users SET member_pic="" WHERE email=%s',(user_email, ))
                else:
                    url = "https://d3r92fcxan8msh.cloudfront.net/trip/" + member_pic
                    sql = 'UPDATE users SET member_pic=%s WHERE email=%s'
                    return edit_db(db, sql, (url, user_email))
        except Exception as e:
            logger.error("err_member_pic(%s):%s", user_email, e)
            
    @staticmethod
    def edit_name(user_email, name):
        try:
            with pool.get_connection() as db:
                sql = 'UPDATE users SET name=%s WHERE email=%s'
                return edit_db(db, sql, (name, user_email))
        except Exception as e:
            logger.error("err_edit_name(%s):%s", user_email, e)
            
    @staticmethod
    def edit_phone(user_email, phone):
        try:
            with pool.get_connection() as db:
                sql = 'UPDATE users SET phone=%s WHERE email=%s'
                return edit_db(db, sql, (phone, user_email))
        except Exception as e:
            logger.error("err_edit_phone(%s):%s", user_email, e)

    @staticmethod
    def edit_password(user_email, old_password, new_password):
        try:
            with pool.get_connection() as db:
                sql = 'UPDATE users set password=%s WHERE email=%s AND password=%s'
                return edit_db(db, sql, (md5(new_password), user_email, md5(old_password)))
        except Exception as e:
            logger.error("err_edit_password(%s):%s", user_email, e)

    @staticmethod
    def get_account(user_email):
        try:
            with pool.get_connection() as db:
                sql = 'SELECT name, email, phone FROM users WHERE email=%s'
                return selectone(db, sql, (user_email, ))
        except Exception as e:
            logger.error("err_get_account(%s):%s", user_email, e)

