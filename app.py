from flask import Flask, render_template
from api.attraction import attraction
from api.user import user
from setting import setting

app = Flask(__name__)
app.config.from_object(setting)
app.jinja_env.auto_reload = True
app.register_blueprint(attraction)
app.register_blueprint(user)    

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=3000)