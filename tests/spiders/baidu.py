"""
Author: xuxiongfeng
Date: 2019-06-13 17:20
Usage: 
"""

import scrapy
from scrapy.crawler import CrawlerProcess


class BaiduSpider(scrapy.Spider):
    name = 'baidu'

    def start_requests(self):
        yield scrapy.Request(url='https://www.baidu.com', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})

    def parse(self, response):
        a_list = response.xpath('//a')
        for a in a_list:
            link = a.xpath('./@href').get()
            text = a.xpath('./text()').get()
            yield {'link': link, 'text': text}


if __name__ == '__main__':
    settings = {'HTTPCACHE_ENABLED': True, 'HTTPCACHE_DIR': '.', 'HTTPCACHE_EXPIRATION_SECS': 60 * 60}
    cp = CrawlerProcess(settings=settings)
    cp.crawl(BaiduSpider)
    cp.start()
