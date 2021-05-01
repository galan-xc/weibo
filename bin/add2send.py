import redis
import ujson

redis_key = "sender:msg"
db_conn = redis.StrictRedis(host="47.98.129.65", port=6379, db=1, password="1690036618")
data = {
    "uid": "5944643324",
    "msg": "Hello World",
}
print(data)
cds = ujson.dumps(data)
db_conn.rpush(redis_key, cds)

db_conn.connection_pool.disconnect()
