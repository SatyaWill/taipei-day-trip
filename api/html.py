from flask import render_template
from api import html

@html.route("/")
def index():
	return render_template("index.html")

@html.route("/verify")
def verify():
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

@html.route("/history")
def history():
	return render_template("history.html")

@html.route("/account")
def account():
	return render_template("account.html")