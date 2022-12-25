from setting import config

# for model, api 裡的各個 .py 連線到"連線池"
pool = config.pool

# for data.db_user.py / db_attraction.py ==> 建table
add = config.add

# for app.py ==> config.from_object(setting)
setting = config.setting

# for model.token_set.py
SECRET_KEY = config.setting.SECRET_KEY
SALT = config.setting.SALT

partner_key = config.setting.partner_key
merchant_id = config.setting.merchant_id