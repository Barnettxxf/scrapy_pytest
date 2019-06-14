"""
Author: xuxiongfeng
Date: 2019-06-14 14:44
Usage: 
"""
import scrapy
from scrapy.http import Response
from scrapy_pytest import env
from scrapy_pytest.factory import RequestFactory, ResponseFactory

from tests.spiders.baidu import BaiduSpider

env.set_httpcache_dir('/Users/barnettxu/Projects/scrapy_pytest/cache')


def test_req_factory():
    req_factory = RequestFactory(BaiduSpider)
    for parse_func, reqs in req_factory.reqs.items():
        assert type(parse_func).__name__ == 'method'
        for req in reqs:
            assert isinstance(req, scrapy.Request)


def test_rsp_factory():
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, response in rsp_factory.gen():
        assert type(parse_func).__name__ == 'method'
        assert isinstance(response, Response)
