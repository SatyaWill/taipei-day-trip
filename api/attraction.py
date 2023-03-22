from flask import Blueprint, request
from api import attraction
from controller import attraction_controller

attraction = Blueprint("attraction", __name__)
controller = attraction_controller.AttractionController
@attraction.route("/api/attractions")
def attractions():
    page = request.args.get('page')
    keyword = request.args.get('keyword')
    return controller.attractions(int(page), keyword)

@attraction.route("/api/attraction/<int:attraction_id>")
def attraction_page(attraction_id):
    return controller.attraction_page(attraction_id)
    
@attraction.route("/api/categories")
def categories():
    return controller.categories()

