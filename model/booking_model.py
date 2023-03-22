from .db import pool, selectone, edit_db
import logging, json
logger = logging.getLogger(__name__)

class BookingModel:
    @staticmethod
    def booking_check(user_email):
        try:
            with pool.get_connection() as db:
                sql = '''SELECT JSON_OBJECT(
                        'attraction', JSON_OBJECT(
                            'id', a.id, 
                            'name', a.name, 
                            'address', a.address,
                            'image', i.image
                        ),
                        'date', DATE_FORMAT(b.date, '%Y-%m-%d'),
                        'time', b.time,
                        'price', b.price,
                        'phone', c.phone
                    ) AS data
                    FROM attractions a
                    INNER JOIN booking b ON a.id = b.att_id
                    INNER JOIN users c ON b.user_email = c.email
                    LEFT JOIN images i ON a.id = i.att_id
                    WHERE b.user_email = %s LIMIT 1'''
                r = selectone(db, sql, (user_email,))
                if r:
                    try:
                        data = json.loads(r["data"])
                    except json.JSONDecodeError:
                        return "Invalid JSON data"
                    return data
                else:
                    return None
        except Exception as e:
            logger.error("err_booking_check(%s):%s", user_email, e)
            return None

    @staticmethod
    def booking_reserve(user_email, id, date, time, price):
        try:
            with pool.get_connection() as db:
                # booking: user_email, att_id, date, time, price
                sql = "REPLACE booking VALUE(%s,%s,%s,%s,%s)"
                data = edit_db(db, sql, (user_email, id, date, time, price))
                return data
        except Exception as e:
            logger.error("err_booking_reserve(%s):%s", user_email, e)
            return None

    @staticmethod
    def booking_delete(user_email):
        try:
            with pool.get_connection() as db:
                return edit_db(db, "DELETE IGNORE FROM booking WHERE user_email = %s", (user_email,))
        except Exception as e:
            logger.error("err_booking_delete(%s):%s", user_email, e)
            return False
