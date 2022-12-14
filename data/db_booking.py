import sys
sys.path.append("..")
from setting import add

add('CREATE TABLE booking( \
  user_email VARCHAR(100) NOT NULL, \
  att_id INT UNSIGNED NOT NULL, \
  date DATE NOT NULL, \
  time ENUM("morning", "afternoon") NOT NULL, \
  price SMALLINT(4) UNSIGNED NOT NULL, \
  PRIMARY KEY (user_email), \
  FOREIGN KEY (att_id) REFERENCES attractions(id) ON DELETE CASCADE ON UPDATE CASCADE\
)')




    

