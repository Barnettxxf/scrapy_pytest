"""
Author: xuxiongfeng
Date: 2019-06-14 11:56
Usage: 
"""
import os
from collections import defaultdict

from scrapy.utils.misc import load_object
import pickle

from .utils.request import request_from_dict
from .settings import Settings


class RequestFactory:
    def __init__(self, spider_cls, settings=None):
        self.spider_cls = spider_cls

        if settings is None:
            settings = Settings()
        if isinstance(settings, dict):
            settings = Settings(settings)

        self.settings = settings

        self._reqeusts = defaultdict(list)
        self.storage = load_object(self.settings['HTTPCACHE_STORAGE'])(self.settings)

    def _gen_request(self):
        for rpath in self.storage.find_request_path(self.spider_cls):
            metadata = self._read_meta(rpath)
            yield request_from_dict(metadata)

    def _read_meta(self, rpath):
        metapath = os.path.join(rpath, 'pickled_meta')
        if not os.path.exists(metapath):
            return  # not found
        with open(metapath, 'rb') as f:
            return pickle.load(f)

    @property
    def reqs(self):
        if len(self._reqeusts) == 0:
            for req in self._gen_request():
                callback = req.callback or self.spider_cls().parse
                self._reqeusts[callback].append(req)

        return self._reqeusts


class ResponseFactory:
    def __init__(self, spider_cls, settings=None):
        self.req_factory = RequestFactory(spider_cls, settings)
        self.spider_cls = spider_cls
        self.storage = self.req_factory.storage

    def gen(self):
        for parse_func, reqs in self.req_factory.reqs.items():
            for req in reqs:
                yield parse_func, self.storage.retrieve_response(self.spider_cls, req)
