"""
Author: xuxiongfeng
Date: 2019-06-14 14:44
Usage: 
"""
import os

import scrapy
from scrapy.http import Response
from scrapy_pytest import env
from scrapy_pytest.factory import RequestFactory, ResponseFactory, TemplateFactory

from cache_dir import cache_dir
from tests.spiders.Wangyi import WangyiSpider
from tests.spiders.baidu import BaiduSpider

env.set_httpcache_dir(cache_dir)


def test_req_factory():
    req_factory = RequestFactory(BaiduSpider)
    for parse_func, reqs in req_factory.reqs.items():
        assert type(parse_func).__name__ == 'method'
        for req in reqs:
            assert isinstance(req, scrapy.Request)


def test_rsp_factory():
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, responses in rsp_factory.gen():
        assert type(parse_func).__name__ == 'method'
        assert isinstance(responses, list)
        for response in responses:
            assert isinstance(response, Response)


def test_tmpl_factory():
    tmpl_factory = TemplateFactory(BaiduSpider)
    tmpl_factory.gen_template()
    tmpl_factory = TemplateFactory(WangyiSpider)
    tmpl_factory.gen_template()


