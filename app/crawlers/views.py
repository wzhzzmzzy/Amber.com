from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app
from . import crawlers
from .forms import UserForm
from xk_crawler.utils import headless_chrome

browser = headless_chrome()


@crawlers.route('/')
def index():
    return render_template('crawlers.html')


@crawlers.route('/xk', methods=['GET', 'POST'])
def xk_crawler():
    import time
    import json
    from pyquery import PyQuery
    from xk_crawler.utils import login_prepare, init_session
    if request.method == 'GET':
        form = UserForm()
        capt_path = str(time.time()) + '.png'
        xk_csrf, xk_cookies = login_prepare('app/static/' + capt_path)
        form.xk_csrf.data = xk_csrf
        form.xk_cookies.data = json.dumps(xk_cookies)
        return render_template('xk.html', form=form, captcha=capt_path)
    if request.method == 'POST':
        form_data = dict([(item[0], item[1][0]) for item in dict(request.form).items()])
        res, xk_session = init_session(form_data)
        doc = PyQuery(res)
        if len(doc('title').text().strip()) > 8:
            flash("密码或验证码错误")
            return redirect(url_for('crawlers.xk_crawler', _external=True))
        else:
            flash("登陆成功")
            cookies_str = json.dumps(xk_session.cookies.get_dict())
            return redirect(url_for('crawlers.xk_crawler_personal',
                                    name=form_data['name'], cookies=cookies_str, xh=form_data['xh'], _external=True))


@crawlers.route('/xk/personal')
def xk_crawler_personal():
    import json
    import requests
    from xk_crawler.crawler import get_gpa, get_project, get_grade_table
    user = {
        'xm': request.args.get('name'),
        'xh': request.args.get('xh')
    }
    xk_session = requests.Session()
    requests.utils.cookiejar_from_dict(json.loads(request.args.get('cookies')), xk_session.cookies)
    table_header, table = get_grade_table(xk_session, user, "全部", "全部", csv_path='app/grade_csv/' + user['xh'] + '.csv')
    print(table_header)
    project = get_project(xk_session, user)
    print(project)
    gpa = get_gpa(table, project)
    print(gpa)
    return render_template('xk_personal.html', xh=user['xh'], gpa=gpa)


@crawlers.route('/xk/csv')
def xk_csv():
    import os
    xh = request.args.get('xh')
    print(current_app.root_path)
    return send_from_directory(os.path.join(current_app.root_path, 'grade_csv'), xh+'.csv', as_attachment=True)


@crawlers.route('/weibo')
def weibo_crawler():
    return render_template('weibo.html')
