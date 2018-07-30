# 正方教务系统（xk.suda.edu.cn）爬虫

## 已实现部分

- 考试成绩单获取
- GPA 查询

## 依赖

- BeautifulSoup 4
- Selenium
- Google Chrome >= 65.0
- Chrome Driver
- PIL
- configparser
- requests

## 目录结构

- `app/` Flask APP
    - `crawlers/`
    - `main/`
- `xk_crawlers/` 爬虫本体
    - `crawler.py` 爬虫业务逻辑，页面分析，数据收集等
    - `utils.py` 爬虫功能支持，Session、Cookies、验证码等