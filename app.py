from flask import Flask
from api.html import html
from api.attraction import attraction
from api.user import user
from api.booking import booking
from setting import setting

app = Flask(__name__)
app.config.from_object(setting)
app.jinja_env.auto_reload = True
app.register_blueprint(html)
app.register_blueprint(attraction)
app.register_blueprint(user)
app.register_blueprint(booking)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=3000)