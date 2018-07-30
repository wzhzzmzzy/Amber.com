from flask import Flask, render_template, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap



from xk_crawler.utils import get_code

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'hardcore'





@app.route('/')
def index():
    return render_template('index.html')





browser = None
xk_session = None
form = None


@app.route('/xk_crawler/xk', methods=['GET'])
def xk_crawler():
    import time
    from xk_crawler.utils import headless_chrome, urls
    from selenium import webdriver
    # browser = headless_chrome()
    browser = webdriver.Chrome()
    browser.get(urls['index'])
    captcha = str(time.time()) + '.png'
    get_code(browser, 'static/' + captcha)
    form = UserForm()
    return render_template('xk.html', form=form, captcha=captcha)


@app.route('/crawlers/xk', methods=['POST'])
def xk_crawler_login():
    global browser
    global xk_session
    global form
    import requests
    from xk_crawler.utils import build_cookie
    name = form.name.data
    xh = form.xh.data
    pwd = form.password.data
    auth = form.captcha.data
    cookies = build_cookie(browser, {
        'xh': xh,
        'pwd': pwd,
        'captcha': auth
    })
    if cookies is not None:
        xk_session = requests.Session()
        requests.utils.cookiejar_from_dict(cookies, xk_session.cookies)
        flash("登陆成功")
    else:
        flash("验证码不正确")
    return redirect(url_for('xk_crawler'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    manager.run()
