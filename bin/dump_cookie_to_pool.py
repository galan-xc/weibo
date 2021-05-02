import pymysql
import os
import requests

host = os.environ.get('MYSQL_HOST', "127.0.0.1")
password = os.environ.get('MYSQL_PASSWORD', "127.0.0.1")
def get_def_mysql_db():
    db = pymysql.connect(host=host, user="root", password=password, database="weibo", port=3306)
    return db

def get_all_cookie(db):
    ret = None
    cursor = db.cursor()
    sql = "select * from cookie;"
    try:
        exe_ret = cursor.execute(sql)
        ret = cursor.fetchall()
    except BaseException as e:
        print(e)
    return ret

def push(tup):
    rsp = requests.get("http://47.98.129.65:8002/cookie_pool/add", params={
        "account": tup[3],
        "password": tup[4],
        "uid": tup[1],
        "cookie": tup[2],
    })
    print(rsp.text)


if __name__ == "__main__":
    tups = []
    with get_def_mysql_db() as db:
        tmp  = get_all_cookie(db)
        if tmp:
            tups = tmp
    for tup in tups:
        push(tup)




