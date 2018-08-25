# -*- coding: utf-8 -*-
import scrapy
import json
import requests


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = []
    proxy_api = 'http://118.25.193.162:12980/crawlers/random'

    def start_requests(self):
        proxy_addr = 'http://' + requests.get(self.proxy_api).text
        yield scrapy.Request(url='http://httpbin.org/get', meta={'proxy': proxy_addr})

    def parse(self, response):
        yield json.loads(response.text)
