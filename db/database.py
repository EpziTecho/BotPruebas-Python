# database.py
import pymysql
import sett  # Asumiendo que tienes configuraciones allí

def get_db_connection():
    return pymysql.connect(host=sett.MYSQL_HOST,
                           user=sett.MYSQL_USER,
                           password=sett.MYSQL_PASSWORD,
                           db=sett.MYSQL_DB,
                           cursorclass=pymysql.cursors.DictCursor)

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        result = cursor.fetchall()
        conn.commit()
    conn.close()
    return (result[0] if result else None) if one else result

def test_db_connection():
    try:
        conn = pymysql.connect(host=sett.MYSQL_HOST,
                               user=sett.MYSQL_USER,
                               password=sett.MYSQL_PASSWORD,
                               db=sett.MYSQL_DB,
                               cursorclass=pymysql.cursors.DictCursor)
        print("Conexión exitosa a la base de datos.")
        conn.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

