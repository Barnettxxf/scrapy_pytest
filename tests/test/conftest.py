"""
Author: xuxiongfeng
Date: 2019-06-13 17:51
Usage: 
"""
import pytest
import scrapy
from scrapy_pytest import format_response_fixture

from tests.spiders.baidu import BaiduSpider, HTTPCACHE_DIR


@pytest.fixture
def response():
    request = scrapy.Request('https://www.baidu.com')
    cachedir = HTTPCACHE_DIR
    return format_response_fixture(BaiduSpider, request, cachedir)
