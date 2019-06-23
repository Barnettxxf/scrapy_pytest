"""
Author: xuxiongfeng
Date: 2019-06-14 11:41
Usage: 
"""

from scrapy_pytest import env
from scrapy_pytest.settings import Settings

from cache_dir import cache_dir


def test_set_httpcache():
    _cache_dir = '/tmp/test_httpcache'
    env.set_httpcache_dir(_cache_dir)
    assert env.get_httpcache_dir() == _cache_dir


def test_update():
    name = 'TESTUPDATENAME'
    value = 'TESTUPDATEVALUE'
    env.update(name, value)
    assert env.get('TESTUPDATENAME') == value


def test_httpcache():
    env.set_httpcache_dir(cache_dir)
    assert Settings().get('HTTPCACHE_DIR') == env.get_httpcache_dir()


def test_settings():
    from scrapy_pytest import env
    print(dict(env.items()))
