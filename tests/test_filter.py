import pytest
from scrapy_pytest import env
from scrapy_pytest.filter import RequestFilter, ResponseFilter

from cache_dir import cache_dir
from tests.spiders.Wangyi import WangyiSpider


@pytest.fixture(autouse=True)
def set_httpcache_dir():
    env.set_httpcache_dir(cache_dir)


def test_request_filter():
    f = RequestFilter(WangyiSpider, 'parse_detail')
    assert len(f['redirect_times__in__meta']) == 2
    assert f['download_timeout__keyin__meta']


def test_response_filter():
    f = ResponseFilter(WangyiSpider, 'parse_detail')
    assert f['301__eq__status']
    assert f['300__gt__status']
    assert f['300__lt__status']
    assert f['aosou__in__url']
