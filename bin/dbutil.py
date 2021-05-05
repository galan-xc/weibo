import pymysql
import os
import datetime

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


def get_exp_cookie(db):
    """
    8小时之前为exp cookie
    """
    ret = None
    cursor = db.cursor()
    sql = 'select * from cookie where update_time < "{}"'.format(
        (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    )
    print(sql)
    try:
        exe_ret = cursor.execute(sql)
        ret = cursor.fetchall()
    except BaseException as e:
        print(e)
    return ret


def get_last_cookie(db):
    ret = None
    cursor = db.cursor()
    sql = 'select * from cookie where update_time > "{}"'.format(
        (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    )
    print(sql)
    try:
        exe_ret = cursor.execute(sql)
        ret = cursor.fetchall()
    except BaseException as e:
        print(e)
    return ret