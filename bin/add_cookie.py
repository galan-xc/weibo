from selenium import webdriver
# from selenium.webdriver.common.proxy import Proxy
# from selenium.webdriver.common.proxy import ProxyType

import time
import requests
import base64
import json
import threading

from dump_cookie_to_pool import get_def_mysql_db, get_all_cookie

cookie_update_url = "http://47.98.129.65:8002/cookie/update"


def get_auth_code(url):
    img_rsp = requests.get(url)
    print(img_rsp)
    # with open("pin.png", 'wb')as fp:
    #     fp.write(img_rsp.content)
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
        PROXY = "127.0.0.1:7890"
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        # option.add_argument('--proxy-server={0}'.format(PROXY))
        option.add_argument('--headless')
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
        time.sleep(1)
        code = self.driver.find_element_by_xpath('//img[@class="checkcode"]')
        code_url = code.get_attribute("src")
        code = get_auth_code(code_url)
        if code:
            self.driver.find_element_by_xpath('//div/input[@id="freecheckcode"]').click()
            self.driver.find_element_by_xpath('//div/input[@id="freecheckcode"]').send_keys(code)
        # 登入
        self.driver.find_element_by_xpath('//div/a[@class="loginBtn"]').click()
        time.sleep(1)
        if "index.php" in self.driver.current_url:
            print("登入成功")
        else:
            with open("error.txt", 'a')as fp:
                fp.write("{}\t{}\n".format(self.username, self.password))
            print("登入失败")
            return False

        # # 等待登入
        # input("输入验证码后按任意键继续!!!")
        cookies = self.driver.get_cookies()
        cookie_dict = {}
        print(cookies)
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        print(cookie_dict)
        return cookie_dict

    def open_weibo(self):
        print("start open weibo...")
        login = self.driver.get("https://weibo.com/")
        time.sleep(2)
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
    if sina.open_weibo():
        sina.update()
    sina.driver.close()


if __name__ == "__main__":
    tups = []
    with get_def_mysql_db() as db:
        tmp = get_all_cookie(db)
        if tmp:
            tups = tmp
    tasks = []
    for tup in tups:
        sina_event(tup[3], tup[4])
        # t = threading.Thread(target=sina_event, args=(tup[3], tup[4]), name=tup[3])
        # tasks.append(t)
        # for task in tasks:
        #     task.start()
        #     task.join()

# sina = Sina("txk4sp@sina.com", "uhg928")
# sina.test_ip()
