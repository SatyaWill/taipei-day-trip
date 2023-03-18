from dotenv import load_dotenv
import os

load_dotenv()
class setting:
    DEBUG = False
    CSRF_ENABLED = True
    JSON_AS_ASCII=False
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    DB_HOST = os.getenv('DB_HOST')
    DB_DB = os.getenv('DB_DB')
    DB_USER = os.getenv('DB_USER')
    DB_PW = os.getenv('DB_PW')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SALT = os.getenv('SALT')
    partner_key = os.getenv('partner_key')
    merchant_id = os.getenv('merchant_id')
    BUCKET = os.getenv('BUCKET')
    REGION = os.getenv('REGION')
    S3_ID = os.getenv('S3_ID')
    S3_KEY = os.getenv('S3_KEY')
    MAIL = os.getenv('MAIL')
    MAIL_PW = os.getenv('MAIL_PW')
    REDIS_HOST = os.getenv('REDIS_HOST')
    VERIFICATION_URL = os.getenv('VERIFICATION_URL')
    
class dev(setting):
    DEVELOPMENT = True
    DEBUG = True
    DB_HOST = os.getenv('DB_HOST1')
    DB_USER = os.getenv('DB_USER1')
    DB_PW = os.getenv('DB_PW1')
    REDIS_HOST = os.getenv('REDIS_HOST1')
    VERIFICATION_URL = os.getenv('VERIFICATION_URL1')


