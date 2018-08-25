# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from zhihu.items import UserCardItem
from urllib import parse

comma2int = lambda s:  int(''.join(s.split(',')))

followee_api_url = 'https://www.zhihu.com/api/v4/members/{}/followees'
follower_api_url = 'https://www.zhihu.com/api/v4/members/{}/followers'
follower_url = 'https://www.zhihu.com/people/{}/followers'
proxy_api = 'http://118.25.193.162:12980/crawlers/random'


class UserSpider(scrapy.Spider):
    name = 'user'

    def start_requests(self):
        start_point = [
            'excited-vczh'
        ]
        headers = {
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        for id in start_point:
            url = "https://www.zhihu.com/people/{}/activities".format(id)
            proxy_addr = 'http://' + requests.get(proxy_api).text
            yield scrapy.Request(url=url, callback=self.parse_user, headers=headers, meta={'id': id, 'download_latency': 1, 'proxy': proxy_addr})

    def parse_user(self, response):
        """
        解析用户主页面 Card，获取姓名、简介、头像、推荐回答数、获赞数、关注数、粉丝数
        :param response:
        :return:
        """
        user = UserCardItem()
        user['id'] = response.meta['id']
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
        user['followee'] = comma2int(follow_card[0])
        user['follower'] = comma2int(follow_card[1])
        yield user
        params = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'limit': '20',
            'offset': ''
        }
        # for offset in range(user['follower'] // 20):
        for offset in range(100, 300): # 爬取范围
            offset *= 20
            params['offset'] = str(offset)
            url = follower_api_url.format(user['id']) + '?' + parse.urlencode(params)
            headers = {
                'Host': 'www.zhihu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
            }
            proxy_addr = 'http://' + requests.get(proxy_api).text
            yield scrapy.Request(url=url, callback=self.parse_followers, headers=headers, meta={'proxy': proxy_addr})

        # TODO: 获取 user['follower'] 之后，访问 https://www.zhihu.com/api/v4/members/excited-vczh/followers 获取用户信息

    def parse_followers(self, response):
        res = json.loads(response.text)
        for data in res['data']:
            if int(data['follower_count']) > 100:
                yield data
