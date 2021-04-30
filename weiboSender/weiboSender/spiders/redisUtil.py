import redis
import ujson
import os
import time


def _serialize_obj(obj):
    try:
        return ujson.dumps(obj)
    except BaseException as e:
        print("ujson.dumps error")


def _unserialize_obj(obj):
    try:
        return ujson.loads(obj)
    except BaseException as e:
        print("ujson.loads error")


class RedisDB(redis.Redis):
    def set_dict(self, k, v, seconds=0):
        if seconds > 0:
            return self.set(k, _serialize_obj(v), seconds)
        else:
            return self.set(k, _serialize_obj(v))

    def get_dict(self, k):
        obj = self.get(k)
        if obj is not None:
            return _unserialize_obj(obj)
        return obj

    def rpush_dict(self, name, obj):
        return self.rpush(name, _serialize_obj(obj))

    def lpush_dict(self, name, obj):
        return self.lpush(name, _serialize_obj(obj))

    def rpop_dict(self, name):
        obj = self.rpop(name)
        if obj is not None:
            return _unserialize_obj(obj)
        return obj

    def lpop_dict(self, name):
        obj = self.lpop(name)
        if obj is not None:
            return _unserialize_obj(obj)
        return obj

    def hset_obj(self, name, k, v):
        return self.hset(name, k, _serialize_obj(v))

    def hget_obj(self, name, k):
        obj = self.hget(name, k)
        if obj is not None:
            return _unserialize_obj(obj)
        return obj


password = os.environ.get('REDIS_PASSWORD', "123456")
host = os.environ.get('REDIS_HOST', "127.0.0.1")


def get_def_redis_db():
    db = None
    try:
        db = RedisDB(host=host, port="6379", db="1", password=password)
    except BaseException as e:
        print("init redis connect error: {}".format(e))
    return db


def get_redis_db(db):
    db = None
    try:
        db = RedisDB(host=host, port="6379", db=db, password=password)
    except BaseException as e:
        print("init redis connect error: {}".format(e))
    return db


alive_cookie_key = "alive_cookie"
exp_key = "EXP"


def is_exp(uid):
    """
    key: EXP_uid
    """
    ret = None
    with get_redis_db("3") as db:
        ret = db.get("{}-{}".format(exp_key, uid))  # 24小时后解禁
    return ret


def get_alive_cookie():
    tmp = None
    ie = None
    print("start....")
    with get_def_redis_db() as db:
        tmp = db.lpop_dict(alive_cookie_key)
        if tmp:
            ie = is_exp(tmp["uid"])
        print("...0")
        print("t i ", tmp, ie)
        while not tmp or ie:
            print("...1")
            time.sleep(3)
            tmp = db.lpop_dict(alive_cookie_key)
            if tmp:
                ie = is_exp(tmp["uid"])
            print("t i ", tmp, ie)
    return tmp


def add_alive_cookie(data):
    with get_def_redis_db() as db:
        db.rpush_dict(alive_cookie_key, data)


def add_to_exp_list(uid):
    """
    key: EXP_uid
    """
    with get_redis_db("3") as db:
        db.set("{}-{}".format(exp_key, uid), 1, 86400)  # 24小时后解禁
