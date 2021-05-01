import requests

url = "http://47.98.129.65:8002/cookie_pool/add"

rsp = requests.get(url, params={
    # "cookie": "SINAGLOBAL=7275690382884.49.1618922819947; _ga=GA1.2.826918709.1619252479; UOR=www.google.com.hk,weibo.com,login.sina.com.cn; _s_tentry=-; Apache=9836430982976.916.1619871180733; ULV=1619871180898:12:1:3:9836430982976.916.1619871180733:1619791118657; login_sid_t=529c1c28eddf445af3516c1869ffa93f; cross_origin_proto=SSL; SCF=Aujwfj7crOcHIYayS-xSmG44wofxAMe5D-fp7pMVEAtTevi9JXkP8hXzlknrE0iYSP3Qr-05R_E7ZOEAk16P9Uo.; SUB=_2A25NiT2mDeRhGeNG7loX-CfEzDiIHXVu_yhurDV8PUNbmtANLRTXkW9NSyouyUx24cs3fk1VdQVFYmIHRAeqdNS2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5WJLIUfr7.Os._AeE2SZj-5JpX5K2hUgL.Fo-RSKnc1h.RS0B2dJLoIpqLxK-LBK-L1-2LxKML1h-LB.BfShM0; ALF=1651409270; SSOLoginState=1619873270; wvr=6; webim_unReadCount=%7B%22time%22%3A1619873329391%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D",
    "cookie": "webim_unReadCount:%7B%22time%22%3A1619878083116%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D;WBtopGlobal_register_version:91c79ed46b5606b9;SINAGLOBAL:7972394541868.464.1619878081295;Apache:7972394541868.464.1619878081295;_s_tentry:-;wb_view_log_5858689874:1920*10801;wvr:6;ALF:1651414069;SUB:_2A25NiRDlDeRhGeNG7loX-CfEzDiIHXVu_wUtrDV8PUNbmtAKLUbwkW9NSyouyYbjzd0zr6kKNzAqRHRSbQPjapzI;SSOLoginState:1619878069;ULV:1619878081419:1:1:1:7972394541868.464.1619878081295:;SUBP:0033WrSXqPxfM725Ws9jqgMF55529P9D9W5WJLIUfr7.Os._AeE2SZj-5JpX5K2hUgL.Fo-RSKnc1h.RS0B2dJLoIpqLxK-LBK-L1-2LxKML1h-LB.BfShM0;SCF:AhKUa42ZBLT9l-CeNq_4R0cMriBMLTU8XQ3BYbeOVqzWFl5DGOLUNJk2asj0a82Juxw9D7ddi9iAH0toGwR9I1o.",
    "account": "alb7rv@sina.com",
    "password": "ymc321",
    "uid": "test",
})
print(rsp.status_code)
print(rsp.text)
