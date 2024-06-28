# /db/models.py
from .database import query_db

def get_driver_idnumbers():
    return query_db("SELECT idNumber FROM driver")

def check_driver_id(id_number):
    query = "SELECT COUNT(1) AS count FROM driver WHERE idNumber = %s"
    result = query_db(query, (id_number,))
    return result and result[0]['count'] > 0
