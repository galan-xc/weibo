import requests

rows = None
with open("300.txt", 'r') as fp:
    rows = fp.readlines()

for row in rows:
    tmp = row.split("----")
    rsp = requests.get("http://47.98.129.65:8002/cookie/add", params={
        "account": tmp[0].strip(),
        "password": tmp[1].strip(),
        "uid": tmp[2].strip(),
        "cookie": tmp[3].strip(),
    })
    print(rsp.status_code)
