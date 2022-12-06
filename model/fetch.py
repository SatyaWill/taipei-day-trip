import mysql.connector.pooling as pooling
import re, os, sys
sys.path.append("..")
from data import app_pw

secret_key = os.urandom(20)
pool = pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 5,
    pool_reset_session = True,
    host = '127.0.0.1',
    database = 'tp_att',
    user='root',
    password = app_pw.pw()
    )

def selectone(sql, val=''): # 讀取SQL一筆資料
    try:
        mydb = pool.get_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()

def selectall(sql, val=''): # 讀取SQL全部資料
    try:
        mydb = pool.get_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()
        
def selectall2(sql, val=''): # 讀取SQL全部資料(修改images格式)
    try:
        mydb = pool.get_connection()
        cursor = mydb.cursor(dictionary=True)
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
                "images": re.findall(r'http.*?[j|p][p|n]g',i['images'])
            })
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mydb.close()

def edit_db(sql, val=''): # 編輯SQL資料
    try:
        mydb = pool.get_connection() # 連到pooeditdbl
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        mydb.commit()
        print("異動筆數", mydb.cursor().rowcount)
    except Exception as e:
        if "mydb" in dir():
            mydb.rollback()
        print(e)
    finally:
        cursor.close()
        mydb.close()