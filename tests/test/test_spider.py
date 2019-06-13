"""
Author: xuxiongfeng
Date: 2019-06-13 17:49
Usage: 
"""
from tests.spiders.baidu import BaiduSpider


def test_parse(response):
    result = BaiduSpider().parse(response)
    for r in result:
        print(r)
