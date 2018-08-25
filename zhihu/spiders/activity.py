# -*- coding: utf-8 -*-
import scrapy


class ActivitySpider(scrapy.Spider):
    name = 'activity'
    params = {
        'after_id': '',
        'desktop': True,
        'limit': 7
    }

    def parse(self, response):
        pass
