# automatically created by scrapy_pytest

import pytest
from scrapy_pytest import factory, env
from tests.spiders.Wangyi import WangyiSpider as _WangyiSpider

env.set_httpcache_dir('/home/barnett/Projects/scrapy_pytest/cache')

rsp_factory = factory.ResponseFactory(_WangyiSpider)

    
@pytest.fixture(scope='session')
def empty():
    yield
    rsp_factory.close()


@pytest.fixture
def WangyiSpider():
    return _WangyiSpider


@pytest.fixture(scope="module", params=rsp_factory.result['parse_detail'])
def parse_detail_response(empty, request):
    if isinstance(request.param, (tuple, list)):
        response = request.param[0]
    else:
        response = request.param
    return response


@pytest.fixture(scope="module", params=rsp_factory.result['parse'])
def parse_response(empty, request):
    if isinstance(request.param, (tuple, list)):
        response = request.param[0]
    else:
        response = request.param
    return response
