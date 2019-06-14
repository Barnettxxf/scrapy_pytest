"""
Author: xuxiongfeng
Date: 2019-06-14 11:41
Usage: 
"""

from scrapy_pytest import env
from scrapy_pytest.settings.default_settings import HTTPCACHE_DIR


def test_get_httpcache():
    cache_dir = env.get_httpcache_dir()
    assert cache_dir == HTTPCACHE_DIR


def test_set_httpcache():
    cache_dir = '/tmp/test_httpcache'
    env.set_httpcache_dir(cache_dir)
    assert env.get_httpcache_dir() == cache_dir


def test_update():
    name = 'TESTUPDATENAME'
    value = 'TESTUPDATEVALUE'
    env.update(name, value)
    assert env.get('TESTUPDATENAME') == value
