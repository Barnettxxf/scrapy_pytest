"""
Author: xuxiongfeng
Date: 2019-06-14 14:44
Usage: 
"""
import os

import pytest
import scrapy
from scrapy.http import Response
from scrapy_pytest import env, storage_class
from scrapy_pytest.factory import RequestFactory, ResponseFactory, TemplateFactory

from cache_dir import cache_dir
from tests.spiders.Wangyi import WangyiSpider
from tests.spiders.baidu import BaiduSpider


@pytest.fixture(autouse=True)
def set_httpcache_dir():
    env.set_httpcache_dir(cache_dir)


def test_req_factory():
    req_factory = RequestFactory(BaiduSpider)
    for parse_func, reqs in req_factory.reqs.items():
        assert parse_func
        for req in reqs:
            assert isinstance(req, scrapy.Request)
    env.update('HTTPCACHE_STORAGE', storage_class['dbm'])
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, responses in rsp_factory.gen():
        assert parse_func
        assert isinstance(responses, list)
        for response in responses:
            assert isinstance(response, Response)


def test_rsp_factory():
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, responses in rsp_factory.gen():
        assert parse_func
        assert isinstance(responses, list)
        for response in responses:
            assert isinstance(response, Response)
    env.update('HTTPCACHE_STORAGE', storage_class['dbm'])
    rsp_factory = ResponseFactory(BaiduSpider)
    for parse_func, responses in rsp_factory.gen():
        assert parse_func
        assert isinstance(responses, list)
        for response in responses:
            assert isinstance(response, Response)


def test_tmpl_factory():
    tmpl_factory = TemplateFactory(BaiduSpider, test_dir_name='auto_gen_tests')
    tmpl_factory.gen_template()
    tmpl_factory = TemplateFactory(WangyiSpider, test_dir_name='auto_gen_tests')
    tmpl_factory.gen_template()
    env.update('HTTPCACHE_STORAGE', storage_class['dbm'])
    tmpl_factory = TemplateFactory(BaiduSpider, test_dir_name='auto_gen_tests')
    tmpl_factory.gen_template()
    tmpl_factory = TemplateFactory(WangyiSpider, test_dir_name='auto_gen_tests')
    tmpl_factory.gen_template()
