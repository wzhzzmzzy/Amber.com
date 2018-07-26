"""
xk.suda.edu.cn 模拟登陆
"""
from bs4 import BeautifulSoup


def get_grade_table(session, user, year='', term='', save=False):
    """
    获取成绩单
    :param session: 带有 Cookie 的 Session 对象
    :param user: 学号、姓名
    :param year: 学年
    :param term: 学期
    :param save: 是否保存到 ./grade.csv
    :return: (表头，表内容)
    """
    from utils import get_referer, save_to_csv
    from utils import headers

    cj_headers = headers.copy()
    cj_headers['Referer'] = get_referer(user, 'cj')
    res = session.get(cj_headers['Referer'], headers=cj_headers)
    bsObj = BeautifulSoup(res.text, "lxml")

    csrf = bsObj.find_all("input", type="hidden")[-1]['value']
    data = {
        '__VIEWSTATE': csrf,
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': '',
        'ddlxn': year,
        'ddlxq': term,
        'btnCx': ' 查  询 '
    }
    res = session.post(cj_headers['Referer'], headers=cj_headers, data=data)
    bsObj = BeautifulSoup(res.text, "lxml")
    grade = bsObj.find("table", class_="datelist").find_all("tr")
    table = [[i.text for i in item.find_all("td")] for item in grade]
    if save:
        save_to_csv('grade.csv', table[0], table[1:])
    return table[0], table[1:]


def get_gpa(grade_table, project=None):
    """
    根据成绩单获取 GPA
    :param grade_table: 成绩单
    :param project: 培养计划，用于过滤
    :return: GPA，保留三位小数
    """
    from decimal import Decimal
    grade_set = {}
    for item in grade_table:
        if item[15] == '\xa0':
            continue
        course = [(item[3], {
            'name': item[3],
            'credit': eval(item[6]),
            'score': eval(item[15])
        })]
        if grade_set.get(item[4]) is None:
            grade_set[item[4]] = dict(course)
        elif grade_set[item[4]].get(item[3]) is not None:
            grade_set[item[4]][item[3]]['score'] = max(course[0][1]['score'], grade_set[item[4]][item[3]]['score'])
        else:
            grade_set[item[4]].update(course)
    if grade_set.get('新生研讨课程') is not None:
        if grade_set.get('通识选修课程') is None:
            grade_set['通识选修课程'] = {}
        grade_set['通识选修课程'].update(grade_set['新生研讨课程'])
        grade_set.pop('新生研讨课程')

    credit_cnt = 0.0
    score_cnt = 0.0
    for item in grade_set.items():
        cata_name = item[0]
        courses = sorted([i[1] for i in item[1].items()], key=lambda d: d['score'], reverse=True)
        part_credit_pro = project.get(cata_name, 100)
        part_credit_cnt = 0.0
        part_score_cnt = 0.0
        for course in courses:
            part_credit_cnt += course['credit']
            if part_credit_cnt > part_credit_pro:
                credit_temp = course['credit'] - (part_credit_cnt - part_credit_pro)
                part_score_cnt += credit_temp * course['score']
                part_credit_cnt = part_credit_pro
            else:
                part_score_cnt += course['credit'] * course['score']
        credit_cnt += part_credit_cnt
        score_cnt += part_score_cnt
    return '{:.3f}'.format(Decimal(str(score_cnt/credit_cnt)))


def get_project(session, user):
    """
    获取培养计划（学分目标）
    :param session: 带有 Session 的对象
    :param user:
    :return:
    """
    from utils import get_referer
    from utils import headers
    import requests
    jh_headers = headers.copy()
    jh_headers['Referer'] = 'http://xk.suda.edu.cn/xs_main.aspx?xh=1627406048'
    res = session.get(get_referer(user, 'jh'), headers=jh_headers)
    bsObj = BeautifulSoup(res.text, "lxml")
    credit = [i.find_all("td") for i in bsObj.find("table", id="DataGrid4").find_all("tr")]
    credit_set = []
    for item in range(1, len(credit)):
        s = [i.text for i in credit[item]]
        if s[1] == '\xa0':
            continue
        credit_set.append((s[0], eval(s[1])))
    credit_set.append(('通识选修课程', 10))
    return dict(credit_set)


if __name__ == '__main__':
    from utils import read_config, init_session
    user, account = read_config('./config/1628404018.ini')
    xk_session = init_session(account, verbose=False)
    grade_table = get_grade_table(xk_session, user, "全部", "全部")
    pro = get_project(xk_session, user)
    gpa = get_gpa(grade_table[1], project=pro)
    print(gpa)