from setting import config

# for app.py ==> config.from_object(setting)
setting = config.setting
dev = config.dev

DB_HOST = config.setting.DB_HOST
DB_DB = config.setting.DB_DB
DB_USER = config.setting.DB_USER
DB_PW = config.setting.DB_PW

# for model.token_set.py
SECRET_KEY = config.setting.SECRET_KEY
SALT = config.setting.SALT

# TapPay
partner_key = config.setting.partner_key
merchant_id = config.setting.merchant_id

# S3
BUCKET = config.setting.BUCKET
REGION = config.setting.REGION
S3_ID = config.setting.S3_ID
S3_KEY = config.setting.S3_KEY

# mail
MAIL = config.setting.MAIL
MAIL_PW = config.setting.MAIL_PW
VERIFICATION_URL = config.setting.VERIFICATION_URL

REDIS_HOST = config.setting.REDIS_HOST