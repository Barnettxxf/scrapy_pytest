"""
Author: xuxiongfeng
Date: 2019-06-13 18:55
Usage: 
"""
from scrapy.extensions.httpcache import FilesystemCacheStorage

from .utils.response import RetrieveResponse
from .settings import Settings


def format_response_fixture(spidercls, request, settings=Settings, storage_cls=FilesystemCacheStorage):
    storage = RetrieveResponse(settings=settings, storage_cls=storage_cls)
    return storage.retrieve_response(spidercls, request)
