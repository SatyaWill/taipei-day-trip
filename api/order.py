from flask import request
from api import order
from controller import order_controller
from utils import token_required

controller = order_controller.OrderController

@order.route("/api/orders", methods=["POST"])
@token_required
def create_order(user_email):
    prime = request.json.get('prime')
    order = request.json.get('order')
    order_email = order["contact"]["email"]
    name = order["contact"]["name"]
    phone = order["contact"]["phone"]
    att_id = order["trip"]["attraction"]["id"]
    return controller.create_order(user_email, prime, order_email, name, phone, att_id)
                
                
@order.route("/api/order/<number>", methods=["GET"])
@token_required
def order_info(user_email, number):
    return controller.order_info(user_email, number)


@order.route("/api/order/history", methods=["GET"])
@token_required
def order_history(user_email):
    return controller.order_history(user_email)
