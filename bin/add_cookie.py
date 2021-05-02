from selenium import webdriver
import time
import requests

cookie_update_url = "http://47.98.129.65:8002/cookie/update"


class Sina:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.init_driver()
        self.weibo_cookie_str = None

    def init_driver(self):
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.driver = webdriver.Chrome(r"D:\customPath\chromedriver.exe")

    # 模拟登陆
    def login_mail(self):
        print("start login mail...")
        login = self.driver.get("https://mail.sina.com.cn/?from=mail")
        # wait 10 seconds if timeout this method will fail
        time.sleep(2)
        print("开始输密码")
        self.driver.find_element_by_xpath('//div/input[@id="freename"]').click()
        self.driver.find_element_by_xpath('//div/input[@id="freename"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//div/input[@id="freepassword"]').click()
        self.driver.find_element_by_xpath('//div/input[@id="freepassword"]').send_keys(self.password)

        self.driver.find_element_by_xpath('//div/a[@class="loginBtn"]').click()
        # 等待登入
        input("输入验证码后按任意键继续!!!")
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
        time.sleep(4)
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


if __name__ == "__main__":
    # sina = Sina("txk4sp@sina.com", "uhg928")
    sina = Sina("dcn9dd@sina.com", "pct263")
    sina.login_mail()
    sina.open_weibo()
    sina.update()
    sina.driver.close()
