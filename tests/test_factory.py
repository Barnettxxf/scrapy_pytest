"""
Author: xuxiongfeng
Date: 2019-06-14 14:44
Usage: 
"""
import os

import scrapy
from scrapy.http import Response
from scrapy_pytest import env
from scrapy_pytest.env import default_settings
from scrapy_pytest.factory import RequestFactory, ResponseFactory

from src.scrapy_pytest.factory import TemplateFactory
from tests.spiders.baidu import BaiduSpider


def test_req_factory():
    env.set_httpcache_dir('/Users/barnettxu/Projects/scrapy_pytest/cache')
    req_factory = RequestFactory(BaiduSpider)
    for parse_func, reqs in req_factory.reqs.items():
        assert type(parse_func).__name__ == 'method'
        for req in reqs:
            assert isinstance(req, scrapy.Request)


def test_rsp_factory():
    env.set_httpcache_dir('/Users/barnettxu/Projects/scrapy_pytest/cache')
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, response in rsp_factory.gen():
        assert type(parse_func).__name__ == 'method'
        assert isinstance(response, Response)


def test_tmpl_factory():
    env.set_httpcache_dir('/Users/barnettxu/Projects/scrapy_pytest/cache')
    tmpl_factory = TemplateFactory(BaiduSpider, os.path.dirname(__file__), settings=default_settings)
    tmpl_factory.gen_template()
