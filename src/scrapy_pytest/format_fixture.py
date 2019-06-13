"""
Author: xuxiongfeng
Date: 2019-06-13 18:55
Usage: 
"""

from src.scrapy_pytest.utils import RetrieveResponse
from src.scrapy_pytest.utils import FilesystemCacheStorage


def format_response_fixture(spidercls, request, cache_dir, storage=FilesystemCacheStorage):
    storage = RetrieveResponse(cache_dir, storagecls=storage)
    return storage.retrieve_response(spidercls, request)
