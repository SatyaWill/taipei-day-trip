import json, re, app_pw, mysql.connector

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

with open("taipei-attractions.json", mode="r") as file:
    data=json.load(file)
TPTrip=data['result']['results']
reg=re.compile(r'https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|png)')
for d in TPTrip:
    sql="INSERT attractions VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(d['_id'],d['name'],d['CAT'],d['description'],d['address'],d['direction'],d['MRT'],d['latitude'],d['longitude'])
    add(sql,val)
    img=reg.findall(d['file'].lower())
    for i in img:
        sql="INSERT img VALUES(%s,%s)"
        val=(d['_id'],i)
        add(sql,val)

    

