import re
from datetime import date, timedelta

class validate:
    @staticmethod
    def email(email):
        res = re.match(r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$", email)
        return bool(res) 
    
    @staticmethod
    def password(password):
        res = re.match("^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$", password)
        return bool(res) 
    
    @staticmethod
    def phone(phone):
        res = re.match("^09\d{8}$", phone)
        return bool(res)

    @staticmethod
    def invalid_date(d):
        now = int(date.today().strftime("%Y%m%d"))
        max = int((date.today()+timedelta(days=61)).strftime("%Y%m%d"))
        res = (d <= now or d > max)
        return res 
    
    @staticmethod
    def signup_data(name, email, password, phone):
        errors = []
        if not name:
            errors.append("未填寫姓名")
        if not validate.email(email):
            errors.append("電子信箱格式錯誤")
        if not validate.password(password):
            errors.append("密碼包含英文字母和數字，長度至少為 6")
        if not validate.phone(phone):
            errors.append("手機號碼格式錯誤")
        return errors if len(errors) > 0 else None
    
    @staticmethod
    def order_data(name, email, phone):
        errors = []
        if not name:
            errors.append("未填寫姓名")
        if not validate.email(email):
            errors.append("電子信箱格式錯誤")
        if not validate.phone(phone):
            errors.append("手機號碼格式錯誤")
        return errors if len(errors) > 0 else None

