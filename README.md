## Amber 的个人网站

已部署，尚未公开。

包含正方教务系统爬虫（`xk_crawler`）和自动维护代理池（`proxypool`）。

### 试运行

```bash
$ pip3 install -r requirements.txt
$ python3 manager.py runserver
```

### 目录结构

- `app/`，Flask
- `proxypool/`，IP 代理池
- `xk_crawler/`，xk.suda 爬虫，API 接口文档请见这里
- `zhihu/`，zhihu.com Scrapy 爬虫
- `config.py`，Flask Config
- `manager.py`，Flask CLI
- `proxy_run.py`，IP 代理池运行入口
- `scrapy.cfg`，Scrapy Config

