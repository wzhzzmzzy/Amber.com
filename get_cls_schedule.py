import requests
import json

data = requests.get('http://127.0.0.1:5000/crawlers/xk_api').json()

with open('temp.png', 'wb') as fb:
    fb.write(requests.get('http://127.0.0.1:5000' + data['auth']).content)

post_data = {
    'xh': '',  # 学号
    'pwd': '',  # 密码
    'auth': input('验证码位于 ./temp.png，请输入：'),  # 验证码
    '_csrf': data['_csrf'],  # 之前 GET 得到的 _csrf（xk.suda 登录需要）
    '_cookies': json.dumps(data['_cookies']),  # 之前 GET 得到的 _cookies（xk.suda 给的 Cookies）
    'year': '2017-2018',  # 需要查询的学年度
    'term': '1'  # 需要查询的学期
}

print(post_data)

res = requests.post('http://127.0.0.1:5000/crawlers/xk_api', data=post_data).json() # 以 Form 形式发送而不是 JSON

print(res)
