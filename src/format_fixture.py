"""
Author: xuxiongfeng
Date: 2019-06-13 18:55
Usage: 
"""

from src.utils.response import RetrieveResponse
from src.utils.storage import FilesystemCacheStorage


def format_response_fixture(spidercls, cache_dir, request, storage=FilesystemCacheStorage):
    storage = RetrieveResponse(cache_dir, storagecls=storage)
    return storage.retrieve_response(spidercls, request)
