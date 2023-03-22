from flask import jsonify
from model import order_model
from utils import validate
from setting import partner_key, merchant_id
from datetime import datetime
import requests, logging
logger = logging.getLogger(__name__)
model = order_model.OrderModel

class OrderController:
    @staticmethod
    def create_order(user_email, prime, order_email, name, phone, att_id):
        try:
            errs = validate.order_data(name, order_email, phone)
            if errs:
                return {"error" : "true", "message": errs}, 400
            else:
                order_number = datetime.now().strftime("%Y%m%d%H%M%S")
                price = model.create_order(user_email, order_number, order_email, name, phone, att_id)
                if price:
                    pay_info = {
                        "prime": prime,
                        "partner_key": partner_key,
                        "merchant_id": merchant_id,
                        "details":"訂單"+order_number,
                        "amount": price,
                        "cardholder": {
                            "phone_number": phone,
                            "name": name,
                            "email": order_email,
                        }
                    }
                    headers = {"Content-Type": "application/json","x-api-key": partner_key}
                    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                    req = requests.post(url,headers=headers,json=pay_info,timeout=30).json()
                    
                    def data(msg):
                        return {"number": order_number, "payment": {"status": req["status"], "message": msg}}
                    
                    if req["status"] == 0:
                        if model.order_status(order_number):
                            return {"data": data("付款成功")}, 200
                    else:
                        return {"data": data("付款失敗，請重新預定行程及付款")}, 200
                    
        except Exception as e:
            logger.error("err_create_order_c(%s):%s", user_email, e)

    @staticmethod
    def order_info(user_email, number):
        try:
            data = model.order_info(user_email, number)
            return jsonify({"data": data}), 200
        except Exception as e:
            logger.error("err_order_info_c(%s):%s", user_email, e)
    
    @staticmethod
    def order_history(user_email):
        try:
            data = model.order_history(user_email)
            return {"data": data}, 200
        except Exception as e:
            logger.error("err_order_history_c(%s):%s", user_email, e)
