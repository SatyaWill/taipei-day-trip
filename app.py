from flask import *
import os, mysql.connector.pooling as pooling, re
from data import app_pw
from model.fetch import *

app = Flask(__name__, static_folder="static", static_url_path="/")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
pool = pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 5,
    pool_reset_session = True,
    host = '127.0.0.1',
    database = 'tp_att',
    user='root',
    password = app_pw.pw()
    )
  
@app.route("/api/attractions")
def att_page():
    page = request.args.get('page')
    keyword = request.args.get('keyword')
    try:
        page = int(page)
        if keyword:
            sql = 'SELECT attractions.*, images FROM attractions left join images on \
            attractions.id=images.att_id WHERE category=%s OR INSTR(name, %s) ORDER BY id LIMIT %s,13'
            res = selectall2(sql, (keyword, keyword ,page*12))
            if len(res) > 12:
                return {"nextPage":page+1,"data":res[0:12]}, 200
            else:
                return {"nextPage":None,"data":res}, 200
        else:
            sql = 'SELECT attractions.*, images FROM attractions left join images on \
                attractions.id=images.att_id ORDER BY id LIMIT %s,13'
            res = selectall2(sql, (page*12,))
            if len(res) > 12:          
                return {"nextPage":page+1,"data":res[0:12]}, 200
            else:
                return {"nextPage":None,"data":res}, 200
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500

@app.route("/api/attraction/<int:attractionId>")
def att(attractionId):
    try:
        sql = 'SELECT attractions.*, images FROM attractions left join images on \
        attractions.id=images.att_id WHERE id=%s'
        res = selectone(sql, (attractionId,))
        if res:
            res['images'] = re.findall(r'http.*?[j|p][p|n]g',res['images'])  
            return {"data":res}, 200
        else:
            return jsonify(error=True, message="景點編號不正確"), 400
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500
    
@app.route("/api/categories")
def categories():
    try:
        sql = 'SELECT category FROM category'
        res = [item['category'] for item in selectall(sql)]
        return {"data":res}, 200
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500

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

app.run(host='0.0.0.0',port=3000,debug=True)
