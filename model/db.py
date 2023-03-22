from setting import DB_HOST, DB_DB, DB_USER, DB_PW
import mysql.connector.pooling, json

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 15,
    pool_reset_session = True,
    host = DB_HOST,
    database = DB_DB,
    user= DB_USER,
    password = DB_PW
)

def selectone(db, sql, val=''): # 讀取SQL一筆資料
    try:
        cursor = db.cursor(dictionary=True)                
        cursor.execute(sql, val)
        return cursor.fetchone()
    except Exception as e:
        print(e)

def selectall(db, sql, val=''): # 讀取SQL全部資料
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchall()
    except Exception as e:
        print(e)

        
def selectall_img(db, sql, val=''): # 讀取SQL全部資料(修改images格式)
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        res=[]
        for i in cursor:
            res.append({
                "id": i["id"],
                "name": i["name"],
                "category": i["category"],
                "description": i["description"],
                "address": i["address"],
                "transport": i["transport"],
                "mrt": i["mrt"],
                "lat": i["lat"],
                "lng": i["lng"],
                "images": json.loads(i['images'])
            })
        return res
    except Exception as e:
        print(e)

def edit_db(db, sql, val=''): # 編輯SQL資料
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        db.commit()
        res = cursor.rowcount
        return res
    except Exception as e:
        if "db" in dir():
            db.rollback()
        print(e)
        
        
def add(sql, val=''): # 建db table
    try:
        db = pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()