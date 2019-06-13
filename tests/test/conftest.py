"""
Author: xuxiongfeng
Date: 2019-06-13 17:51
Usage: 
"""
import pytest
import scrapy

from src.format_fixture import format_response_fixture
from tests.spiders.baidu import BaiduSpider


@pytest.fixture
def response():
    request = scrapy.Request('https://www.baidu.com')
    cachedir = '/Users/barnettxu/Projects/scrapy_pytest/tests/spiders/.scrapy'
    return format_response_fixture(BaiduSpider, cachedir, request)
