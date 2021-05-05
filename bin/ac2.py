from selenium import webdriver
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType

import time
import requests
import base64
import json
import threading

from dbutil import get_def_mysql_db, get_all_cookie, get_last_cookie, get_exp_cookie

cookie_update_url = "http://47.98.129.65:8002/cookie/update"


def get_auth_code(url):
    img_rsp = requests.get(url)
    print(img_rsp)
    base_data = base64.encodebytes(img_rsp.content)
    data = {"username": "muyibei", "password": "ababy982028", "typeid": 3, "image": base_data.decode()}
    ocr_rsp = requests.post("http://api.ttshitu.com/predict", json=data)
    rsp_date = json.loads(ocr_rsp.content)
    print(rsp_date)
    if rsp_date["success"]:
        return rsp_date["data"]["result"]
    return None


class Sina:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.init_driver()
        self.weibo_cookie_str = None

    def init_driver(self):
        PROXY = "http://127.0.0.1:7890"
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        # option.add_argument('--proxy-server={0}'.format(PROXY))
        # option.add_argument('--headless')
        self.driver = webdriver.Chrome(r"D:\customPath\chromedriver.exe", chrome_options=option)
        # self.driver = webdriver.Chrome(r"D:\customPath\chromedriver.exe")

    def test_ip(self):
        page = self.driver.get("http://httpbin.org/ip")

    # 模拟登陆
    def login_mail(self):
        print("start login mail...")
        login = self.driver.get("https://mail.sina.com.cn/?from=mail")
        # wait 10 seconds if timeout this method will fail
        time.sleep(1)
        print("开始输密码")
        self.driver.find_element_by_xpath('//div/input[@id="freename"]').click()
        self.driver.find_element_by_xpath('//div/input[@id="freename"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//div/input[@id="freepassword"]').click()
        self.driver.find_element_by_xpath('//div/input[@id="freepassword"]').send_keys(self.password)

        # 点击登入召唤验证码
        self.driver.find_element_by_xpath('//div/a[@class="loginBtn"]').click()
        time.sleep(2)
        try:
            code = self.driver.find_element_by_xpath('//img[@class="checkcode"]')
            code_url = code.get_attribute("src")
            get_code_url_retry = 3
            while not code_url and get_code_url_retry > 0:
                print("retry get code url", get_code_url_retry)
                get_code_url_retry -= 1
                code_url = code.get_attribute("src")
                time.sleep(2)
            code = get_auth_code(code_url)
            if code:
                self.driver.find_element_by_xpath('//div/input[@id="freecheckcode"]').click()
                self.driver.find_element_by_xpath('//div/input[@id="freecheckcode"]').send_keys(code)
            # 登入
            self.driver.find_element_by_xpath('//div/a[@class="loginBtn"]').click()
        except BaseException as e:
            print(e)
        time.sleep(1)

    def open_weibo(self):
        print("start open weibo...")
        login = self.driver.get("https://weibo.com/")
        input("按任意键继续")
        cookies = self.driver.get_cookies()
        cookie_dict = {}
        print(cookies)
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        print(cookie_dict)
        cookie_str = ""
        for cookie in cookie_dict:
            cookie_str += "{}:{};".format(cookie, cookie_dict[cookie])
        print(cookie_str)
        self.weibo_cookie_str = cookie_str

    def update(self):
        rsp = requests.get(url=cookie_update_url, params={
            "account": self.username,
            "cookie": self.weibo_cookie_str,
        })
        print("update rsp-> ", rsp.text)


def sina_event(account, password):
    print(account, password)
    sina = Sina(account, password)

    sina.login_mail()
    sina.open_weibo()
    sina.update()
    sina.driver.close()


if __name__ == "__main__":
    tups = []
    with get_def_mysql_db() as db:
        tmp = get_exp_cookie(db)
        if tmp:
            tups = tmp
    tasks = []
    for tup in tups:
        print(tup)
        sina_event(tup[3], tup[4])
        # t = threading.Thread(target=sina_event, args=(tup[3], tup[4]), name=tup[3])
        # tasks.append(t)
        # for task in tasks:
        #     task.start()
        #     task.join()

# sina = Sina("txk4sp@sina.com", "uhg928")
# sina.test_ip()
