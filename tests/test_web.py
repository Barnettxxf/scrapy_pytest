from scrapy_pytest.web.common import get_responses
from scrapy_pytest import env

from cache_dir import cache_dir


def test_web_utils():
    env.set_httpcache_dir(cache_dir)
    responses = get_responses()
    print()