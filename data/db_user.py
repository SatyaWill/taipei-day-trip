import sys
sys.path.append("..")
from model import add

# 會員資料庫
add("DROP TABLE IF EXISTS users")
add('''CREATE TABLE users (
  id bigint NOT NULL AUTO_INCREMENT, 
  name varchar(50) NOT NULL, 
  email varchar(100) NOT NULL, 
  phone char(10),
  password char(32) NOT NULL,
  member_pic char(100) NOT NULL,
  time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY (id), 
  UNIQUE KEY email (email) 
)''')




    

