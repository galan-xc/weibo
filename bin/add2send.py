import redis
import ujson

redis_key = "sender:msg"
db_conn = redis.StrictRedis(host="47.98.129.65", port=6379, db=1, password="1690036618")
cookie_str = "SUB=_2A25NhJ0uDeRhGeNG7loX-CbMyjmIHXVuhiNmrDV6PUNbktANLRfekW1NSyojgZpz6NNtwNs3Fp1VKN-js1DVqE0A; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF3DPr6xeGb_JWzTziap7ea5JpX5K2hUgL.Fo-RSKnc1hn7eK-2dJLoIpqLxKqLBK2L1KeLxKqL1-eLBKnpeoeX; SSOLoginState=1619062142; _T_WM=48576091800;"

data = {
    "uid": "5985057641",
    "msg": "TD",
}
print(data)
cds = ujson.dumps(data)
db_conn.rpush(redis_key, cds)

db_conn.connection_pool.disconnect()
