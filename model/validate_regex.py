import re

def validate_email(email):
    res = re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,4}$", email)
    return bool(res) 

def validate_password(password):
    res = re.match("^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$", password)
    return bool(res) 

def validate_phone(phone):
    res = re.match("^09\d{8}$", phone)
    return bool(res) 