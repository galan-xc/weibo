import redis
import ujson
import os


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


def get_def_redis_db():
    db = None
    try:
        db = RedisDB(host="127.0.0.1", port="6379", db="1", password=password)
    except BaseException as e:
        print("init redis connect error: {}".format(e))
    return db
