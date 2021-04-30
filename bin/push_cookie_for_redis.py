import requests

url = "http://47.98.129.65:8002/cookie_pool/add"

rsp = requests.get(url, params={
    "cookie": "_T_WM=57893099478; XSRF-TOKEN=02ff1d; WEIBOCN_FROM=1110006030; SCF=AsPY6JrKoY3faJFPL3kSg028Df20E5smyVGWW8cBk3jEVGPnWuRO6Sa53I7T37Vqoa5mLo7C8jH_IrQ-k06V0-4.; SUB=_2A25Nj7RsDeRhGeNG7loX-CbOzD6IHXVvc9wkrDV6PUJbktANLVjhkW1NSyoscXmgww0-Wdo_Mjh506r8GZDZl1Qw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKH0RWMbfJz-oJeyvO2ufe5NHD95Qf1h-RSonReoMEWs4Dqcjni--ciKnRiKnRi--ci-8hi-20i--ciKnNiKyWSK57eo5t; SSOLoginState=1619772476; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174",
    "account": "alb7rv@sina.com ",
    "password": "ymc321",
    "uid": "test",
})
print(rsp.status_code)
print(rsp.text)