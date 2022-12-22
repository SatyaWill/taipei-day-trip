from flask import Flask, render_template
from api.html import html
from api.attraction import attraction
from api.user import user
from api.booking import booking
from api.order import order
from setting import setting

app = Flask(__name__)
app.config.from_object(setting)
app.jinja_env.auto_reload = True
app.register_blueprint(html)
app.register_blueprint(attraction)
app.register_blueprint(user)
app.register_blueprint(booking)
app.register_blueprint(order)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404
    
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=3000)