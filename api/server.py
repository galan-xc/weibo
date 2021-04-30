import os

from flask import Flask
from flask import request
import hashlib
import datetime
from utils.logUtil import logger
from utils.redisUtil import get_def_redis_db
from utils.dbUtil import get_def_mysql_db
from utils.retUtil import InfoRet, ErrorRet

app = Flask(__name__)

cookie_list_key = os.environ.get('REDIS_COOKIE_LIST_KEY', "redis_cookie_list")


@app.route("/cookie/add")
def add_cookie():
    params = request.args

    if "cookie" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "account" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "password" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "uid" not in params:
        return ErrorRet(msg="Missing required parameter")
    tmp = params.to_dict()
    ret = -1
    cookie_str = params.get("cookie")
    md5_obj = hashlib.md5()
    md5_obj.update(cookie_str.encode("utf-8"))
    cuid = md5_obj.hexdigest()
    account = params.get("account")
    password = params.get("password")
    uid = params.get("uid")

    with get_def_mysql_db() as db:
        cursor = db.cursor()
        sql = "insert into cookie(cuid, uid, account, password, cookie_str, create_time)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s')" % (
                  cuid, uid, account, password, cookie_str, datetime.datetime.now()
              )
        try:
            ret = cursor.execute(sql)
            db.commit()
        except BaseException as e:
            tmp.update({
                "ret": ret,
                "uid": uid,
            })
            return ErrorRet(data=tmp, msg=str(e))
            db.rollback()
    tmp.update({
        "ret": ret,
        "uid": uid,
    })
    return InfoRet(tmp)


@app.route("/cookie/len")
def len_cookie():
    length = -1
    ret = -1
    with get_def_mysql_db() as db:
        cursor = db.cursor()
        sql = "SELECT count(id) FROM `cookie`;"
        try:
            ret = cursor.execute(sql)
            length = cursor.fetchone()
        except BaseException as e:
            return ErrorRet(msg=str(e))
    return InfoRet({
        "length": length,
        "ret": ret
    })

alive_cookie_key = "alive_cookie"
exp_key = "EXP"

@app.route("/cookie_pool/add")
def add_cookie_pool():
    params = request.args
    if "cookie" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "account" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "password" not in params:
        return ErrorRet(msg="Missing required parameter")
    if "uid" not in params:
        return ErrorRet(msg="Missing required parameter")
    cookie_str = params.get("cookie")
    cookie_list = cookie_str.split(";")
    cookie = {}
    for c in cookie_list:
        tmp = c.partition("=")
        cookie[tmp[0].strip()] = tmp[2].strip()
    data = {
        "to_dict": cookie,
        "account": params.get("account"),
        "uid": params.get("uid"),
        "password": params.get("password"),
    }
    with get_def_redis_db() as db:
        db.rpush_dict(alive_cookie_key, data)
    return InfoRet(params)

@app.route("/cookie_pool/len")
def len_cookie_pool():
    length = -1
    with get_def_redis_db() as db:
        length = db.llen(alive_cookie_key)
    return InfoRet({"length": length})

if __name__ == "__main__":
    app.run("0.0.0.0", 8002, debug=True)
