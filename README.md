## Amber 的个人网站

已部署，尚未公开。

包含正方教务系统爬虫（`xk_crawler`）和自动维护代理池（`proxypool`）。

### 试运行

```bash
$ pip3 install -r requirements.txt
$ python3 manager.py runserver
```

### 课表 API

可以通过 API 来获取课表的网页源码（TODO：将源码改成 JSON）

#### API 接受的表单格式

```
{
    'xh': '',   # 学号
    'pwd': '',  # 密码
    'auth': '', # 验证码
    '_csrf': '',      # GET 得到 _csrf（xk.suda 登录需要）
    '_cookies': '',   # GET 得到 _cookies（xk.suda 给的 Cookies）
    'year': '2017-2018',  # 需要查询的学年度
    'term': '1'           # 需要查询的学期
}
```

#### API 返回的 JSON 格式

```
{
    'name': '',             # 姓名
    'major': '',            # 专业
    'college': '',          # 学院
    'class_schedule': ''    # 课程表网页源码
}
```

#### API 请求示例

```python
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

res = requests.post('http://127.0.0.1:5000/crawlers/xk_api', data=post_data).json() # 以 Form 形式发送而不是 JSON
```

