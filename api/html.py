from flask import Blueprint, render_template

html = Blueprint('html', __name__)

@html.route("/")
def index():
	return render_template("index.html")

@html.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")

@html.route("/booking")
def booking():
	return render_template("booking.html")

@html.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")