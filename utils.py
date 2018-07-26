urls = {
    'index': "http://xk.suda.edu.cn/",                  # 首页
    'home': "http://xk.suda.edu.cn/default_szdx.aspx",  # 用户首页
    'kb': "http://xk.suda.edu.cn/xskbcx.aspx",          # 课表
    'cj': "http://xk.suda.edu.cn/xscjcx_dq.aspx",       # 成绩
    'jh': "http://xk.suda.edu.cn/pyjh.aspx",            # 培养计划（每年推荐选课）
    'xk': "http://xk.suda.edu.cn/xsxkqk.aspx",          # 选课情况
    'ks': "http://xk.suda.edu.cn/xskscx.aspx"           # 考试时间
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Host': "xk.suda.edu.cn"
}

post_data = {
    "__VIEWSTATE":"",       # CSRF
    "__EVENTTARGET": "",    # 修改字段名 固定
    "__EVENTARGUMENT": "",  # 未知字段 固定
    "ddlXN": "",            # 学年
    "ddlXQ": "",            # 学期
    "btnCx": " 查  询 "      # 按钮 固定
}

params = {
    'kb': {'xh': "", "xm": "", 'gnmkdm':"N121603"},
    'cj': {'xh': "", "xm": "", 'gnmkdm':"N121604"},
    'jh': {'xh': "", "xm": "", 'gnmkdm':"N121607"},
    'xk': {'xh': "", "xm": "", 'gnmkdm':"N121610"},
    'ks': {'xh': "", "xm": "", 'gnmkdm':"N121615"}
}


def wttn():
    """
    What's the time now?
    :return: int(%yymmdd)
    """
    import datetime

    now = datetime.datetime.now()
    return int(str(now.year) + str(now.month) + str(now.day))


def headless_chrome():
    """
    Chrome Headless Mode With Selenium
    :return: Selenium Chrome Driver
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_opt = Options()
    chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--disable-gpu')
    return webdriver.Chrome(chrome_options=chrome_opt)


# def process_captcha(img):
#     """
#     Read Image Captcha With Tesseract-OCR
#     :param img: Pillow Image
#     :return: Captcha String
#     """
#     try:
#         import tesserocr
#         from PIL import Image
#     except ImportError:
#         print("This method needs Tesserocr & PIL")
#         return
#     # img = img.convert('L')
#     threshold = 150
#     img_table = []
#     for i in range(256):
#         img_table.append(0 if i < threshold else 1)
#     img = img.point(img_table, '1')
#     img.show()
#     return tesserocr.image_to_text(img)


def get_code(browser):
    """
    save screenshot and crop the captcha
    :return:
    """
    import os
    from PIL import Image
    browser.save_screenshot('temp.png')
    code_ele = browser.find_element_by_id('icode')
    left = code_ele.location['x']
    top = code_ele.location['y']
    right = code_ele.location['x'] + code_ele.size['width']
    bottom = code_ele.location['y'] + code_ele.size['height']
    os.remove('temp.png')
    return Image.open('temp.png').crop((left, top, right, bottom))


def build_cookie(account, verbose=True):
    """
    Try to Login xk.suda.edu.cn and Get Cookies
    :return: Selenium Cookies
    """
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import UnexpectedAlertPresentException
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver

    cookie_got = False
    browser = webdriver.Chrome() if verbose else headless_chrome()
    wait = WebDriverWait(browser, 10)
    browser.get(urls['index'])
    xh_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TextBox1')))
    pwd_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TextBox2')))
    xh_input.send_keys(account['xh'])
    pwd_input.send_keys(account['pwd'])
    while not cookie_got:
        try:
            captcha_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TextBox3')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Button1')))
            get_code(browser).show()
            captcha = input("请输入验证码：")
            captcha_input.clear()
            captcha_input.send_keys(captcha)
            submit.click()
            browser.page_source # 用于当验证码错误时报出异常
            cookie_got = True
            chrome_cookies = browser.get_cookies()
            cookies = {}
            for cookie in chrome_cookies:
                cookies[cookie['name']] = cookie['value']
            save_cookies(account['xh'], cookies)
            return cookies
        except UnexpectedAlertPresentException:
            browser.switch_to.alert.accept()


def find_cookie_from_mongo(account, db):
    """
    Get Cookies that hasn't expired from MongoDB
    :return: Cookies dict-like
    """

    return db['cookies'].find_one({
        'account': account,
        'expires': {'$gte': wttn()}
    })['cookies']


def save_cookies(xh, cookies):
    import json
    import sys
    with open(sys.path[0] + '/cookies/' + xh + '.json', "w") as json_f:
        json.dump(cookies, json_f)


def read_cookies(xh):
    from json import load
    from sys import path
    from os.path import exists
    from os import stat
    from datetime import datetime
    import time
    cookie_path = path[0] + '/cookies/' + xh + '.json'
    if not exists(cookie_path):
        return False
    loc_t = datetime.now()
    modi_t = time.localtime(stat(cookie_path).st_mtime)
    modi_t = datetime(modi_t.tm_year, modi_t.tm_mon, modi_t.tm_mday, modi_t.tm_hour, modi_t.tm_min, modi_t.tm_sec)
    if (loc_t-modi_t).seconds > 1200:
        return False
    with open(cookie_path) as json_f:
        return load(json_f)


def get_referer(user, page_flag):
    from urllib import parse

    data = params[page_flag].copy()
    data['xh'] = user['xh']
    data['xm'] = user['xm']
    return urls[page_flag] + '?' + parse.urlencode(data)


def read_config(filename):
    from configparser import ConfigParser
    conf = ConfigParser()
    conf.read(filename)
    user = dict(conf.items('User'))
    account = dict(conf.items('Account'))
    return user, account


def init_session(account, verbose=True):
    import requests
    cookies = read_cookies(account['xh'])
    if not cookies:
        cookies = build_cookie(account, verbose)
    session = requests.Session()
    requests.utils.cookiejar_from_dict(cookies, session.cookies)
    return session


def save_to_csv(filename, header, table):
    import csv
    with open(filename, "w", encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(table)


if __name__ == '__main__':
    print(read_cookies('1627406048'))