# -*- coding: utf-8 -*-
import scrapy
from zhihu.items import UserCardItem

comma2int = lambda s:  int(''.join(s.split(',')))


class UserSpider(scrapy.Spider):
    name = 'user'

    def start_requests(self):
        headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        start_point = [
            'excited-vczh'
        ]
        home_urls = ("https://www.zhihu.com/people/{}/activities".format(name) for name in start_point)
        follow_urls = ("https://www.zhihu.com/people/{}/followers".format(name) for name in start_point)
        for url in home_urls:
            yield scrapy.Request(url=url, callback=self.parse_user, headers=headers)
        for url in follow_urls:
            yield scrapy.Request(url=url, callback=self.parse_followers, headers=headers)

    def parse_user(self, response):
        """
        解析用户主页面 Card，获取姓名、简介、头像、推荐回答数、获赞数、关注数、粉丝数
        :param response:
        :return:
        """
        user = UserCardItem()
        user['name'] = response.css('.ProfileHeader-name::text').extract_first()
        user['brief'] = response.css('.ProfileHeader-headline::text').extract_first()
        user['avatar'] = response.css('.Avatar::attr("src")').extract_first()
        achievement = response.css('.Profile-sideColumnItems')
        try:
            user['recommend_answer'] = comma2int(achievement.re('(\d+)\s个回答')[0])
        except:
            user['recommend_answer'] = 0
        user['star'] = comma2int(achievement.re('获得.*?([0-9,]+).*?次赞同')[0])
        follow_card = response.css('.NumberBoard-itemValue::text').extract()
        user['follow'] = comma2int(follow_card[0])
        user['follower'] = comma2int(follow_card[1])
        yield user
        # TODO: 获取 user['follower'] 之后，访问 https://www.zhihu.com/api/v4/members/excited-vczh/followers 获取用户信息

    def parse_followers(self, response):
        pass
