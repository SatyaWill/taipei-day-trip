import sys
sys.path.append("..")
from model import add

# 會員資料庫
add("DROP TABLE IF EXISTS orders")
add('''CREATE TABLE orders (
  order_number CHAR(14) NOT NULL PRIMARY KEY,
  status BIT(1) NOT NULL,
  user_email VARCHAR(100) NOT NULL, 
  order_email VARCHAR(100) NOT NULL, 
  name VARCHAR(50) NOT NULL,
  phone CHAR(10) NOT NULL,
  att_id INT UNSIGNED NOT NULL, 
  date DATE NOT NULL, 
  time ENUM("morning", "afternoon") NOT NULL, 
  price SMALLINT(4) UNSIGNED NOT NULL, 
  FOREIGN KEY (att_id) REFERENCES attractions(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE ON UPDATE CASCADE
)''')




    

