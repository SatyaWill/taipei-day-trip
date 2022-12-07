from flask import Blueprint, request, jsonify
import re, sys
sys.path.append("..")
from model import selectall, selectall_img, selectone

attraction = Blueprint('attraction', __name__)

@attraction.route("/api/attractions")
def att_page():
    page = request.args.get('page')
    keyword = request.args.get('keyword')
    try:
        page = int(page)
        if keyword:
            sql = 'SELECT attractions.*, images FROM attractions left join images on \
            attractions.id=images.att_id WHERE category=%s OR INSTR(name, %s) ORDER BY id LIMIT %s,13'
            res = selectall_img(sql, (keyword, keyword ,page*12))
            if len(res) > 12:
                return {"nextPage":page+1,"data":res[0:12]}, 200
            else:
                return {"nextPage":None,"data":res}, 200
        else:
            sql = 'SELECT attractions.*, images FROM attractions left join images on \
                attractions.id=images.att_id ORDER BY id LIMIT %s,13'
            res = selectall_img(sql, (page*12,))
            if len(res) > 12:          
                return {"nextPage":page+1,"data":res[0:12]}, 200
            else:
                return {"nextPage":None,"data":res}, 200
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500

@attraction.route("/api/attraction/<int:attractionId>")
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
    
@attraction.route("/api/categories")
def categories():
    try:
        sql = 'SELECT category FROM category'
        res = [item['category'] for item in selectall(sql)]
        return {"data":res}, 200
    except Exception as e:
        print(e)
        return jsonify(error=True, message="伺服器內部錯誤"), 500