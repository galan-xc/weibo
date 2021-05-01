import requests

rsp = requests.post("https://api.weibo.com/webim/2/direct_messages/new.json", headers={
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "136",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "SINAGLOBAL=7275690382884.49.1618922819947; _ga=GA1.2.826918709.1619252479; UOR=www.google.com.hk,weibo.com,login.sina.com.cn; _s_tentry=-; Apache=9836430982976.916.1619871180733; ULV=1619871180898:12:1:3:9836430982976.916.1619871180733:1619791118657; login_sid_t=529c1c28eddf445af3516c1869ffa93f; cross_origin_proto=SSL; SCF=Aujwfj7crOcHIYayS-xSmG44wofxAMe5D-fp7pMVEAtTevi9JXkP8hXzlknrE0iYSP3Qr-05R_E7ZOEAk16P9Uo.; SUB=_2A25NiT2mDeRhGeNG7loX-CfEzDiIHXVu_yhurDV8PUNbmtANLRTXkW9NSyouyUx24cs3fk1VdQVFYmIHRAeqdNS2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5WJLIUfr7.Os._AeE2SZj-5JpX5K2hUgL.Fo-RSKnc1h.RS0B2dJLoIpqLxK-LBK-L1-2LxKML1h-LB.BfShM0; ALF=1651409270; SSOLoginState=1619873270; wvr=6; webim_unReadCount=%7B%22time%22%3A1619873329391%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D",
    "Host": "api.weibo.com",
    "Origin": "https://api.weibo.com",
    "Referer": "https://api.weibo.com/chat/",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
}, data={
    "text": "30",
    "uid": "5944643324",
    "extensions": '{"clientid":""}',
    "is_encoded": "0",
    "decodetime": "1",
    "source": "209678993",
})
print(rsp)
print(rsp.status_code)
print(rsp.text)
