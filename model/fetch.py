import re
import sys
sys.path.append("..")
from setting import pool

def selectone(sql, val=''): # 讀取SQL一筆資料
    try:
        db = pool.get_connection() # 連到pool
        cursor = db.cursor(dictionary=True)                
        cursor.execute(sql, val)
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def selectall(sql, val=''): # 讀取SQL全部資料
    try:
        db = pool.get_connection() # 連到pool
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
        
def selectall_img(sql, val=''): # 讀取SQL全部資料(修改images格式)
    try:
        db = pool.get_connection() # 連到pool
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
                "images": re.findall(r'http.*?[j|p][p|n]g',i['images'])
            })
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

def edit_db(sql, val=''): # 編輯SQL資料
    try:
        db = pool.get_connection() # 連到pool
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        db.commit()
        res = cursor.rowcount
        return res
    except Exception as e:
        if "db" in dir():
            db.rollback()
        print(e)
    finally:
        cursor.close()
        db.close()