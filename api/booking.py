from flask import Blueprint, request
import sys 
sys.path.append("..") 
from model import edit_db, selectone, token_required

booking = Blueprint('booking', __name__)

@booking.route("/api/booking", methods=["GET"])
@token_required
def booking_check(user_email):
    if user_email:
        sql = "SELECT a.id, a.name, a.address, \
            SUBSTRING_INDEX(b.images, ',' , 1) image, \
            DATE_FORMAT(c.date, '%Y-%m-%d') date, c.time, c.price \
            FROM attractions a, images b, booking c \
            WHERE c.user_email = %s AND \
            a.id = c.att_id AND b.att_id = c.att_id"
        r = selectone(sql, (user_email,))
        if r:
            attraction = {
                "id":r["id"], 
                "name": r["name"], 
                "address": r["address"],
                "image": r["image"]
                }
            data = {
                "attraction":attraction, 
                "date": r["date"], 
                "time": r["time"], 
                "price": r["price"]
                }
            return {"data": data}, 200
        else:
            return {"data": None}, 200

@booking.route("/api/booking", methods=["POST"])
@token_required
def booking_reserve(user_email):
    id = int(request.json.get('attractionId'))
    date = request.json.get('date')
    time = request.json.get('time')
    price = request.json.get('price')
    if user_email:
        # booking: user_email, att_id, date, time, price
        sql = "REPLACE booking VALUE(%s,%s,%s,%s,%s)"
        edit_db(sql, (user_email, id, date, time, price))
        return {"ok":True}, 200
    
@booking.route("/api/booking", methods=["DELETE"])
@token_required
def booking_delete(user_email):
    if user_email:
        edit_db("DELETE IGNORE FROM booking WHERE user_email = %s", (user_email,))
        return {"ok":True}, 200
