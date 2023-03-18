from flask import request
from controller import booking_controller
from api import booking
from utils import token_required

controller = booking_controller.BookingController

@booking.route("/api/booking", methods=["GET"])
@token_required
def booking_check(user_email):
    return controller.booking_check(user_email)

@booking.route("/api/booking", methods=["POST"])
@token_required
def booking_reserve(user_email):
    id = int(request.json.get('attractionId'))
    date = request.json.get('date')
    time = request.json.get('time')
    price = request.json.get('price')
    return controller.booking_reserve(user_email, id, date, time, price)
    
@booking.route("/api/booking", methods=["DELETE"])
@token_required
def booking_delete(user_email):
    return controller.booking_delete(user_email)

