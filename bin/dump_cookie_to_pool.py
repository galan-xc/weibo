import requests
from dbutil import get_def_mysql_db, get_all_cookie


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
        tmp = get_all_cookie(db)
        if tmp:
            tups = tmp
    for tup in tups:
        push(tup)
