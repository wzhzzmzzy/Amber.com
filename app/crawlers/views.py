from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app, jsonify, g
from . import crawlers
from .forms import UserForm, ClassForm
from proxypool.db import RedisClient


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@crawlers.route('/')
def index():
    return render_template('crawlers.html')


@crawlers.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@crawlers.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


@crawlers.route('/xk', methods=['GET', 'POST'])
def xk_crawler():
    import time
    import json
    from pyquery import PyQuery
    from xk_crawler.utils import login_prepare_splash, init_session
    from xk_crawler.crawler import get_name
    if request.method == 'GET':
        form = UserForm()
        capt_path = str(time.time()) + '.png'
        xk_csrf, xk_cookies = login_prepare_splash('app/static/' + capt_path)
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
            name = get_name(xk_session, form_data['xh'])
            cookies_str = json.dumps(xk_session.cookies.get_dict())
            return redirect(url_for('crawlers.xk_crawler_personal',
                                    name=name, cookies=cookies_str, xh=form_data['xh'], _external=True))


@crawlers.route('/xk/personal', methods=['GET', 'POST'])
def xk_crawler_personal():
    import json
    import requests
    from xk_crawler.crawler import get_gpa, get_grade_table, get_project, get_cls_schedule
    user = {
        'xm': request.args.get('name'),
        'xh': request.args.get('xh')
    }
    xk_session = requests.Session()
    requests.utils.cookiejar_from_dict(json.loads(request.args.get('cookies')), xk_session.cookies)
    if request.method == 'GET':
        kb_form = ClassForm()
        table_header, table = get_grade_table(xk_session, user, csv_path='app/grade_csv/' + user['xh'] + '.csv')
        project = get_project(xk_session, user)
        gpa = get_gpa(table, project)
        return render_template('xk_personal.html', xh=user['xh'], gpa=gpa, kb_form=kb_form)
    if request.method == 'POST':
        form_data = dict([(item[0], item[1][0]) for item in dict(request.form).items()])
        tb_filename = 'app/cls_table/' + user['xh'] + '_' + form_data['year'] + '_' + form_data['term'] + '.html'
        get_cls_schedule(xk_session, user, year=form_data['year'], term=form_data['term'], html_path=tb_filename)
        return redirect(url_for('crawlers.xk_crawler_cls_schedule',
                                xh=user['xh'], year=form_data['year'], term=form_data['term']))


@crawlers.route('/xk/cls_schedule')
def xk_crawler_cls_schedule():
    xh = request.args.get('xh')
    year = request.args.get('year')
    term = request.args.get('term')
    tb_filename = 'app/cls_table/' + xh + '_' + year + '_' + term + '.html'
    with open(tb_filename) as f:
        content = f.read()
    return render_template('cls_schedule.html', content=content)


@crawlers.route('/xk/csv')
def xk_csv():
    import os
    xh = request.args.get('xh')
    return send_from_directory(os.path.join(current_app.root_path, 'grade_csv'), xh+'.csv', as_attachment=True)


@crawlers.route('/xk/cls_schedule')
def xk_cls_schedule():
    import os
    xh = request.args.get('xh')
    return send_from_directory(os.path.join(current_app.root_path, 'cls_table'), xh+'.html', as_attachment=True)


@crawlers.route('/zhihu')
def zhihu_crawler():
    return render_template('zhihu.html')


@crawlers.route('/xk_api', methods=['GET', 'POST'])
def xk_api_login():
    import time
    from pyquery import PyQuery
    from xk_crawler.utils import login_prepare, init_session
    from xk_crawler.crawler import get_name, get_college, get_cls_schedule
    if request.method == 'GET':
        capt_path = str(time.time()) + '.png'
        xk_csrf, xk_cookies = login_prepare('app/static/' + capt_path)
        return jsonify({
            'auth': url_for('static', filename=capt_path),
            '_csrf': xk_csrf,
            '_cookies': xk_cookies
        })
    if request.method == 'POST':

        form_data = {
            'xh': request.form['xh'],
            'pwd': request.form['pwd'],
            'auth': request.form['auth'],
            'xk_csrf': request.form['_csrf'],
            'xk_cookies': request.form['_cookies'],
            'year': request.form['year'],
            'term': request.form['term']
        }
        print(form_data)
        res, xk_session = init_session(form_data)
        doc = PyQuery(res)
        if len(doc('title').text().strip()) > 8:
            return jsonify({'error': '密码或验证码错误'})
        else:
            user = {
                'xm': get_name(xk_session, form_data['xh']),
                'xh': form_data['xh']
            }
            detail = get_college(xk_session, user)
            cls_schedule = get_cls_schedule(xk_session, user, form_data['year'], form_data['term'])
            return jsonify({
                'name': user['xm'],
                'major': detail[1],
                'college': detail[0],
                'class_schedule': cls_schedule
            })

