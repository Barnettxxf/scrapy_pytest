# automatically created by scrapy_pytest


import pytest
from scrapy_pytest import factory, env
from tests.spiders.baidu import BaiduSpider as _BaiduSpider

env.set_httpcache_dir('/home/barnett/Projects/scrapy_pytest/cache')

rsp_factory = factory.ResponseFactory(_BaiduSpider)


@pytest.fixture(scope='session')
def empty(request):
    request.addfinalizer(rsp_factory.close)


@pytest.fixture
def BaiduSpider():
    return _BaiduSpider


@pytest.fixture(scope="module", params=rsp_factory.result['parse'])
def parse_response(empty, request):
    if isinstance(request.param, (tuple, list)):
        response = request.param[0]
    else:
        response = request.param
    return response
