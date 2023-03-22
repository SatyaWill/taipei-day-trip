from utils.validate import validate

def test_email():
    assert validate.email("john.doe@example.com") == True
    assert validate.email("jane_doe-123@example.co.uk") == True
    assert validate.email("john.doe@.com") == False
    assert validate.email("jane_doe@example..com") == False

def test_password():
    # 正確的密碼格式
    assert validate.password("abc123") == True
    assert validate.password("abc123def") == True
    
    # 錯誤的密碼格式
    assert validate.password("abc") == False
    assert validate.password("123456") == False

def test_phone():
    # 正確的手機號碼格式
    assert validate.phone("0912345678") == True
    assert validate.phone("09123456789") == False
    assert validate.phone("09123456") == False
    assert validate.phone("09123456aa") == False

def test_order_data():
    # 測試訂單表單資料
    assert validate.order_data("John Doe", "john.doe@example.com", "0912345678") == None
    assert validate.order_data("", "jane_doe@example.co.uk", "0922123456") == ["未填寫姓名"]
    assert validate.order_data("Bob Smith", "bob@invalid..email", "09123456789") == ["電子信箱格式錯誤", "手機號碼格式錯誤"]