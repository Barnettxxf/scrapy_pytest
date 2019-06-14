"""
Author: xuxiongfeng
Date: 2019-06-13 17:20
Usage: 
"""
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_pytest import env

from cache_dir import cache_dir


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'

    def start_requests(self):
        yield scrapy.Request(url='https://news.163.com/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

    def parse(self, response):
        a_list = response.xpath('//a')
        for i, a in enumerate(a_list):
            link = a.xpath('./@href').get()
            text = a.xpath('./text()').get()
            if link.startswith('http'):
                yield scrapy.Request(url=link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'},
                                     callback=self.parse_detail)
            if i == 6:
                break
            yield {'link': link, 'text': text}

    def parse_detail(self, response):
        a_list = response.xpath('//a')
        for a in a_list:
            link = a.xpath('./@href').get()
            text = a.xpath('./text()').get()
            yield {'link': link, 'text': text}


if __name__ == '__main__':
    settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': cache_dir,
        'HTTPCACHE_STORAGE': env.get('HTTPCACHE_STORAGE')
    }
    cp = CrawlerProcess(settings=settings)
    cp.crawl(WangyiSpider)
    cp.start()
