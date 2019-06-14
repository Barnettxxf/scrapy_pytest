import pytest
from scrapy_pytest import factory, env
from tests.spiders.Wangyi import WangyiSpider as _WangyiSpider

env.set_httpcache_dir('/home/barnett/Projects/scrapy_pytest/cache')

rsp_factory = factory.ResponseFactory(_WangyiSpider)


@pytest.fixture
def WangyiSpider():
    return _WangyiSpider


@pytest.fixture
def parse_detail_response():
    return rsp_factory.result['parse_detail']


@pytest.fixture
def parse_response():
    return rsp_factory.result['parse']
