from model import booking_model
from utils import validate
import logging
logger = logging.getLogger(__name__)
model = booking_model.BookingModel

class BookingController:
    @staticmethod
    def booking_check(user_email):
        try:
            data = model.booking_check(user_email)
            return {"data": data}, 200
        except Exception as e:
            logger.error("err_booking_check_c(%s):%s", user_email, e)
    
    @staticmethod
    def booking_reserve(user_email, id, date, time, price):
        try:
            if "-" not in date:
                return {"error":True, "message":"日期格式不正確"}, 400
            if validate.invalid_date(int(date.replace("-",""))):
                return {"error":True, "message":"日期錯誤"}, 400
            if model.booking_reserve(user_email, id, date, time, price):
                return {"ok":True}, 200
        except Exception as e:
            logger.error("err_booking_reserve_c(%s):%s", user_email, e)
            
    @staticmethod
    def booking_delete(user_email):
        try:
            if model.booking_delete(user_email):
                return {"ok":True}, 200
        except Exception as e:
            logger.error("err_booking_delete_c(%s):%s", user_email, e)


