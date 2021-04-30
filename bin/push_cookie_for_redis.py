import requests

url = "http://47.98.129.65:8002/cookie_pool/add"

rsp = requests.get(url, params={
    "cookie": "_T_WM=48979361789; MLOGIN=0; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Zf1xpbq0eXUk8mR7iBB5y5NHD95Qf1Ke41Kz4eh.EWs4Dqcjdi--Ni-24iKnci--ciK.RiK.0i--fiKyhiK.N; SUB=_2A25NjjFRDeRhGeNH6FsY8ifMwj6IHXVvcV8ZrDV6PUJbktB-LUKtkW1NSq2pql22i3sZBpOuMRy-2FAXtYAfDN-n; SSOLoginState=1619673345",
    # "cookie": "SUB=_2A25Nj4lrDeRhGeNH6FsY8ifMwj6IHXVvcxcjrDV6PUJbkdAKLUfikW1NSq2pqhUZjhma1wWiNQMAcCHYgJmK9MyD; _T_WM=14943259774; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174; WEIBOCN_FROM=1110006030; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1619764369,1619767485,1619786047,1619786115; XSRF-TOKEN=16b4c4; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1619788095",
    # "cookie": "_T_WM=57893099478;SUB=_2A25Nj7RsDeRhGeNG7loX-CbOzD6IHXVvc9wkrDV6PUJbktANLVjhkW1NSyoscXmgww0-Wdo_Mjh506r8GZDZl1Qw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKH0RWMbfJz-oJeyvO2ufe5NHD95Qf1h-RSonReoMEWs4Dqcjni--ciKnRiKnRi--ci-8hi-20i--ciKnNiKyWSK57eo5t; SSOLoginState=1619772476; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174",
    "account": "alb7rv@sina.com ",
    "password": "ymc321",
    "uid": "test",
})
print(rsp.status_code)
print(rsp.text)