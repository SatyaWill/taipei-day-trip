from flask import Blueprint, request
from datetime import datetime
import sys, requests
sys.path.append("..") 
from setting import partner_key, merchant_id
from model import edit_db, selectone, token_required, validate_email, validate_phone

order = Blueprint('order', __name__)

@order.route("/api/orders", methods=["POST"])
@token_required
def create_order(user_email):
    prime = request.json.get('prime')
    order = request.json.get('order')
    order_email = order["contact"]["email"]
    name = order["contact"]["name"]
    phone = order["contact"]["phone"]
    att_id = order["trip"]["attraction"]["id"]
    is_match = (validate_email(order_email) and validate_phone(phone))
    if not is_match:
        return {"error" : "true", "message":"信箱或手機格式不符"}, 400
    if user_email:
        order_number = datetime.now().strftime("%Y%m%d%H%M%S")
        # orders: order_number,status(0:成功 1:失敗),user_email,
        #         order_email,name,phone,att_id,date,time,price
        sql = '''SELECT DATE_FORMAT(date, '%Y-%m-%d') date, time, price 
            FROM booking WHERE user_email = %s'''
        r = selectone(sql, (user_email,))
        
        sql1 = "REPLACE orders VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (order_number,1, user_email, order_email, name, phone,
               att_id, r['date'], r['time'], r['price'])
        res = edit_db(sql1, val)
        print("更新:",res)
        if not res:
            return {"error":"true", "message":"資料格式異常"}, 400
        else:
            edit_db("DELETE IGNORE FROM booking WHERE user_email = %s", (user_email,))
            pay_info = {
                "prime": prime,
                "partner_key": partner_key,
                "merchant_id": merchant_id,
                "details":"訂單"+order_number,
                "amount": r['price'],
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
                payment = {"status": req["status"], "message": msg}
                return {"number": order_number, "payment": payment}
                       
            if req["status"] == 0:
                res2 = edit_db("UPDATE orders SET status=0 WHERE order_number=%s", (order_number,))
                print("更新:",res2,";付款成功")
                return {"data": data("付款成功")}, 200
            else:
                return {"data": data("付款失敗，請重新預定行程及付款")}, 200
                
                
@order.route("/api/order/<number>", methods=["GET"])
@token_required
def order_info(user_email, number):
    if user_email:
        # orders: order_number,status(0:成功 1:失敗),user_email,
        #         order_email,name,phone,att_id,date,time,price
        sql = '''SELECT a.id, a.name att_name, a.address, 
            SUBSTRING_INDEX(b.images, ',' , 1) image, 
            DATE_FORMAT(c.date, '%Y-%m-%d') date, c.time, 
            c.price, c.status, c.order_email, c.name, c.phone
            FROM attractions a, images b, orders c 
            WHERE c.order_number = %s AND c.user_email = %s 
            AND a.id = c.att_id AND b.att_id = c.att_id'''
        r = selectone(sql, (number, user_email))
        if r:
            attraction = {
                "id":r["id"], 
                "name": r["att_name"], 
                "address": r["address"],
                "image": r["image"]
                }
            trip = {
                "attraction": attraction, 
                "date": r["date"], 
                "time": r["time"], 
                }
            concact = {
                "name": r["name"],
                "email": r["order_email"],
                "phone": r["phone"]
            }
            data = {
                "number": number,
                "price": r["price"],
                "trip": trip,
                "contact": concact,
                "status": r["status"]
            }
            return {"data": data}, 200
        else:
            return {"data": None}, 200