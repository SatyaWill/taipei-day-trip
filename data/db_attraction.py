import json, re
import sys
sys.path.append("..")
from model import add

add("DROP TABLE IF EXISTS category")
add('DROP TABLE IF EXISTS images')
add('DROP TABLE IF EXISTS attractions')
add('''CREATE TABLE attractions (
  id int unsigned NOT NULL,
  name varchar(30) NOT NULL,
  category char(4) NOT NULL,
  description varchar(3000) DEFAULT NULL,
  address varchar(255) NOT NULL,
  transport varchar(500) DEFAULT NULL,
  mrt varchar(10) DEFAULT NULL,
  lat float DEFAULT NULL,
  lng float DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY name (name),
  KEY category (category)
)''')
add('''CREATE TABLE images (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  att_id INT UNSIGNED NOT NULL,
  image varchar(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY(att_id) REFERENCES attractions(id) ON DELETE CASCADE ON UPDATE CASCADE
)''')

with open("taipei-attractions.json", mode="r") as file:
    data=json.load(file)
    TPTrip=data['result']['results']
    reg=re.compile(r'https?://(?:[a-z0-9-]+.)+[a-z]{2,6}(?:/[^/#?]+)+.(?:jpg|png)')
    for d in TPTrip:
        sql="INSERT attractions VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(d['_id'],d['name'],d['CAT'],d['description'],d['address'],d['direction'],d['MRT'],d['latitude'],d['longitude'])
        add(sql,val)
        img=reg.findall(d['file'].lower())
        for i in img:
            sql="INSERT images(att_id, image) VALUES(%s,%s)"
            val=(d['_id'],i)
            add(sql,val)

add("CREATE TABLE category SELECT DISTINCT category FROM attractions ORDER BY category DESC")
