import requests

url = "http://127.0.0.1:8002/cookie_pool/add"

rsp = requests.get(url, params={
    "cookie": "SUB=_2A25NhJ0uDeRhGeNG7loX-CbMyjmIHXVuhiNmrDV6PUNbktANLRfekW1NSyojgZpz6NNtwNs3Fp1VKN-js1DVqE0A; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF3DPr6xeGb_JWzTziap7ea5JpX5K2hUgL.Fo-RSKnc1hn7eK-2dJLoIpqLxKqLBK2L1KeLxKqL1-eLBKnpeoeX; SSOLoginState=1619062142; _T_WM=48576091800;",
    "account": "asdsad",
    "password": "asdsadas",
    "uid": "sadsadsa",
})
print(rsp.status_code)
print(rsp.text)