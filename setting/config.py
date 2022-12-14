from dotenv import load_dotenv
import mysql.connector.pooling as pooling, os

load_dotenv()

pool = pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 5,
    pool_reset_session = True,
    host = '127.0.0.1',
    database = 'tp_att',
    user='root',
    password = os.getenv('DB_PW')
    )

def add(sql, val=''): # 建db table
    try:
        db = pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, val)
        db.commit()
    except Exception as e:
        print(e)

class setting:
    JSON_AS_ASCII=False
    DEBUG= True
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SALT = os.getenv('SALT')


