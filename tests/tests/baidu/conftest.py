import pytest
from scrapy_pytest import factory, env
from tests.spiders.baidu import BaiduSpider as _BaiduSpider

env.set_httpcache_dir('/home/barnett/Projects/scrapy_pytest/cache')

rsp_factory = factory.ResponseFactory(_BaiduSpider)


@pytest.fixture
def BaiduSpider():
    return _BaiduSpider


@pytest.fixture
def parse_response():
    return rsp_factory.result['parse']
