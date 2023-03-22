from flask import jsonify
from model import attraction_model
import logging
logger = logging.getLogger(__name__)

model = attraction_model.AttractionModel

class AttractionController:
    @staticmethod
    def attractions(page, keyword): 
        try:
            res = model.attractions(page, keyword)
            next_page = page + 1 if len(res) == 13 else None
            data = res[0:12]
            return {"nextPage":next_page, "data": data}, 200
        except Exception as e:
            logger.error("err_attractions_c:%s", e)
            return jsonify(error=True, message="伺服器內部錯誤"), 500
    
    @staticmethod 
    def attraction_page(attraction_id):
        try:
            res = model.attraction_page(attraction_id)
            if not res:
                return {"error": True, "message": "景點編號不正確"}, 400
            return {"data": res}, 200
        except Exception as e:
            logger.error("err_attraction_c:%s", e)
            return jsonify(error=True, message="伺服器內部錯誤"), 500
    
    @staticmethod 
    def categories():
        try:
            res = model.categories()
            return {"data":res}, 200
        except Exception as e:
            logger.error("err_categories_c:%s", e)
            return jsonify(error=True, message="伺服器內部錯誤"), 500