from flask import Blueprint
attraction = Blueprint("attraction", __name__)
user = Blueprint("user", __name__)
booking = Blueprint("booking", __name__)
order = Blueprint("order", __name__)
html = Blueprint("html", __name__)

# 註冊Blueprint
def register_blueprints(app):
    from api.attraction import attraction
    from api.user import user
    from api.booking import booking
    from api.order import order
    from api.html import html
    app.register_blueprint(attraction)
    app.register_blueprint(user)
    app.register_blueprint(booking)
    app.register_blueprint(order)
    app.register_blueprint(html)
