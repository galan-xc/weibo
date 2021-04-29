import requests

rows = None
with open("190.txt", 'r') as fp:
    rows = fp.readlines()

for row in rows:
    tmp = row.split("----")
    requests.get("http://47.98.129.65:8002/cookie/add", params={
        "account": tmp[0].strip(),
        "password": tmp[0].strip(),
        "cookie": tmp[0].strip(),
    })
