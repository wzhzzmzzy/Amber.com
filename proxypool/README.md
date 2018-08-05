# 自动维护代理池

## 依赖

- Python>=3.5
- Redis

## 使用

- 安装 Python3 依赖
```
$ pip3 install -r proxy_req.txt
```

- 到`setting.py`中进行 Redis 的配置。

## 运行

```python
from scheduler import Scheduler

Scheduler().run()
```

## 获取代理

```python
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```
