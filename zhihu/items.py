# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserCardItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    brief = scrapy.Field()
    avatar = scrapy.Field()
    recommend_answer = scrapy.Field()
    star = scrapy.Field()
    followee = scrapy.Field()
    follower = scrapy.Field()
