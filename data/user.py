import app_pw, mysql.connector

conn =  mysql.connector.connect(
    host = '127.0.0.1',
    port = '3306',
    database = 'tp_att',
    user='root',
    password = app_pw.pw()
    )
cursor = conn.cursor(dictionary=True)

def add(sql, val=''): # 編輯SQL資料
    try:
        cursor.execute(sql, val)
        conn.commit()
    except Exception as e:
        print(e)

# 會員資料庫
add('CREATE TABLE users (\
  id bigint NOT NULL AUTO_INCREMENT, \
  name varchar(50) NOT NULL, \
  email varchar(100) NOT NULL, \
  password char(32) NOT NULL, \
  time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, \
  PRIMARY KEY (id), \
  UNIQUE KEY email (email) \
)')




    

