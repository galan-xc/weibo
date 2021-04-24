import os

from flask import Flask
from flask import request

from utils.logUtil import logger
from utils.redisUtil import get_def_redis_db
from utils.retUtil import InfoRet, ErrorRet

app = Flask(__name__)

cookie_list_key = os.environ.get('REDIS_COOKIE_LIST_KEY', "redis_cookie_list")


@app.route("/cookie/add")
def add_cookie():
    params = request.args
    if "cookie" not in params:
        return ErrorRet(msg="Missing required parameter")
    cookie_str = params.get("cookie")
    cookie_list = cookie_str.split(";")
    cookie = {}
    for c in cookie_list:
        tmp = c.partition("=")
        cookie[tmp[0].strip()] = tmp[2].strip()
    with get_def_redis_db() as db:
        db.rpush_dict(cookie_list_key, cookie)

    return InfoRet(params)


if __name__ == "__main__":
    app.run("0.0.0.0", 8002, debug=True)
