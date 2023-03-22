from flask import Flask, render_template
from api import register_blueprints
from setting import setting

app = Flask(__name__, template_folder='templates')
app.config.from_object(setting)
app.jinja_env.auto_reload = True
register_blueprints(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
