import redis
import ujson

redis_key = "sender:msg"
db_conn = redis.StrictRedis(host="127.0.0.1", port=6379, db=1, password="password")
data = {
    "uid": "uid",
    "msg": "TD"
}
cds = ujson.dumps(data)
db_conn.rpush(redis_key, cds)

db_conn.connection_pool.disconnect()
