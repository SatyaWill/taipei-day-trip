from .db import pool, selectone, selectall, selectall_img
import logging, re
logger = logging.getLogger(__name__)

class AttractionModel:
    @staticmethod
    def attractions(page, keyword):
        try:
            with pool.get_connection() as db:
                sql = '''WITH att AS (SELECT * FROM attractions 
                        WHERE (%s IS NULL OR category=%s) 
                        OR (%s IS NOT NULL AND INSTR(name, %s)) 
                        ORDER BY id LIMIT %s,13),
                img AS (SELECT att_id, JSON_Arrayagg(image) images 
                        FROM images, att WHERE images.att_id=att.id group by images.att_id)
                SELECT att.*, images FROM att LEFT JOIN img ON img.att_id=att.id'''
                return selectall_img(db, sql, (keyword, keyword, keyword, keyword, page*12))
        except Exception as e:
            logger.error("err_attractions:%s", e)
            return False
            
    @staticmethod 
    def attraction_page(attraction_id):
        try:
            with pool.get_connection() as db:
                sql = '''WITH att_images AS (SELECT att_id, JSON_ARRAYAGG(image) images 
                FROM images WHERE att_id=%s GROUP BY att_id)
                SELECT attractions.*, att_images.images FROM attractions LEFT JOIN att_images ON 
                attractions.id = att_images.att_id WHERE id=%s'''
                res = selectone(db, sql, (attraction_id, attraction_id))
                if res:
                    res['images'] = re.findall(r'http.*?[j|p][p|n]g',res['images'])  
                    return res
                else:
                    return False
        except Exception as e:
            logger.error("err_attraction:%s", e)
            return False
        
    @staticmethod 
    def categories():
        try:
            with pool.get_connection() as db:
                sql = 'SELECT category FROM category'
                return [item['category'] for item in selectall(db, sql)]
        except Exception as e:
            logger.error("err_categories:%s", e)
            return False

        

