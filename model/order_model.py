from .db import pool, selectone, edit_db, selectall
import logging, json
logger = logging.getLogger(__name__)

class OrderModel:          
    @staticmethod
    def create_order(user_email, order_number, order_email, name, phone, att_id):
        try:
            with pool.get_connection() as db:              
                sql0 = '''SELECT 
                    DATE_FORMAT(date, %s) date, 
                    time, 
                    price 
                FROM booking 
                WHERE user_email = %s'''
                r = selectone(db, sql0, ('%Y-%m-%d', user_email))
                # order_number, status(0:成功 1:失敗), user_email, order_email, 
                # name, phone, att_id, date, time, price
                sql = 'REPLACE orders VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                val = (int(order_number),1, user_email, order_email, name, phone, att_id, r['date'], r['time'], r['price'])
                res = edit_db(db, sql, val)
                if res:
                    edit_db(db, "DELETE IGNORE FROM booking WHERE user_email = %s", (user_email,))
                    return r['price']
                else:
                    return False
        except Exception as e:
            logger.error("err_create_order(%s):%s", user_email, e)
            return False
            
    @staticmethod
    def order_status(order_number):
        try:
            with pool.get_connection() as db:
                return edit_db(db, "UPDATE orders SET status=0 WHERE order_number=%s", (order_number,))
        except Exception as e:
            logger.error("err_order_status(%s):%s", order_number, e)
            return False
        
    @staticmethod
    def order_info(user_email, number):
        try:
            with pool.get_connection() as db:   
                # orders: order_number,status(0:成功 1:失敗),user_email,
                #         order_email,name,phone,att_id,date,time,price
                sql = '''SELECT JSON_OBJECT(
                                'number', o.order_number,
                                'price', o.price,
                                'status', CAST(o.status AS SIGNED),
                                'trip', JSON_OBJECT(
                                    'attraction', JSON_OBJECT(
                                        'id', a.id,
                                        'name', a.name,
                                        'address', a.address,
                                        'image', i.image
                                    ),
                                    'date', DATE_FORMAT(o.date, '%Y-%m-%d'),
                                    'time', o.time
                                ),
                                'contact', JSON_OBJECT(
                                    'name', o.name,
                                    'email', o.order_email,
                                    'phone', o.phone
                                )
                            ) AS data
                            FROM orders o
                            INNER JOIN attractions a ON o.att_id = a.id
                            LEFT JOIN images i ON a.id = i.att_id
                            WHERE o.order_number = %s AND o.user_email = %s LIMIT 1'''
                r = selectone(db, sql, (number, user_email))
                if r:
                    return json.loads(r["data"])
                else:
                    return None
        except Exception as e:
            logger.error("err_order_info(%s):%s", user_email, e)
            return None
        
    @staticmethod
    def order_history(user_email):
        try:
            with pool.get_connection() as db:  
                # orders: order_number,status(0:成功 1:失敗),user_email,
                #         order_email,name,phone,att_id,date,time,price
                sql = '''
                    SELECT 
                        o.att_id AS id, 
                        a.name att_name, 
                        a.address, 
                        o.order_number, 
                        DATE_FORMAT(o.date, '%Y-%m-%d') date, 
                        o.time, 
                        o.price, 
                        o.order_email, 
                        o.name, 
                        o.phone, 
                        images.image
                    FROM orders o
                    LEFT JOIN attractions a
                        ON a.id=o.att_id 
                    LEFT JOIN images
                        ON images.att_id=o.att_id 
                    WHERE user_email = %s  AND status=0
                    GROUP BY images.att_id'''
                data = selectall(db, sql, (user_email,))
                if data:
                    return data
                else:
                    return None
        except Exception as e:
            logger.error("err_order_history(%s):%s", user_email, e)
            return None