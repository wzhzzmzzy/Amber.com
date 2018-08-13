# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserCardItem(scrapy.Item):
    name = scrapy.Field()
    brief = scrapy.Field()
    avatar = scrapy.Field()
    recommend_answer = scrapy.Field()
    star = scrapy.Field()
    follow = scrapy.Field()
    follower = scrapy.Field()
