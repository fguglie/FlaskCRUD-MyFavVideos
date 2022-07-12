from tokenize import String
from colorama import Cursor
from flaskext.mysql import MySQL
from config import Config
from typing import Any, Iterator, List, Optional
from app import Flask


var = ''
db = Flask(__name__)
mysql = MySQL()
db.config['MYSQL_DATABASE_HOST']='127.0.0.1'
db.config['MYSQL_DATABASE_USER']='root'
db.config['MYSQL_DATABASE_PASSWORD']=''
db.config['MYSQL_DATABASE_DB']='tpo2python'
mysql.init_app(db)

def _open_cursor() ->Cursor:
    conn    = mysql.connect()
    cursor  = conn.cursor()
    return cursor, conn

def _close_cursor(conn: mysql, cursor: Cursor) -> None:
    conn.commit()
    cursor.close

def _fetch_one(query : str, parameters : Optional[List[str]] = None) ->Any:
    if parameters is None:
        parameters = []
    
    cursor,conn = _open_cursor()

    cursor.execute(query,parameters)
    result  = cursor.fetchone()
    
    _close_cursor(conn, cursor)
    return result

def _fetch_all(query : str, parameters : Optional[List[str]] = None) ->Any:
    if parameters is None:
        parameters = []
    
    cursor,conn = _open_cursor()

    cursor.execute(query,parameters)
    result  = cursor.fetchall()
    
    _close_cursor(conn, cursor)
    return result