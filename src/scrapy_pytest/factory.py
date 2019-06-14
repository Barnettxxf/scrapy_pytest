"""
Author: xuxiongfeng
Date: 2019-06-14 11:56
Usage: 
"""
import os
from collections import defaultdict

from scrapy.utils.misc import load_object
import pickle

from .utils.templates import create_subfile, tmpl_fixture, tmpl_fixture_import, \
    tmpl_parse_func, tmpl_fixture_spider, create_init
from . import RetrieveResponse
from .utils.request import request_from_dict
from .env import Settings


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
            yield request_from_dict(metadata, self.spider_cls)

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
        self.storage = RetrieveResponse(settings or self.req_factory.settings)
        self.filter_set = set()
        self._result = {}

    def gen(self):
        for parse_func, reqs in self.req_factory.reqs.items():
            for req in reqs:
                if parse_func in self.filter_set:
                    continue
                self.filter_set.add(parse_func)
                yield parse_func, self.storage.retrieve_response(
                    self.spider_cls, req)

    @property
    def result(self):
        if len(self._result) == 0:
            for parse_func, rsp in self.gen():
                if parse_func not in self._result.keys():
                    self._result[parse_func.__name__] = rsp
        return self._result


class TemplateFactory:
    def __init__(self, spider_cls, project_dir, settings=Settings(), test_dir_name='tests'):
        self.rsp_factory = ResponseFactory(spider_cls, settings)
        self.project_dir = project_dir
        self.test_dir_name = test_dir_name
        self.spider_cls = spider_cls

        test_dir = os.path.join(self.project_dir, self.test_dir_name)
        create_init(test_dir)
        self.test_spider_dir = os.path.join(test_dir, self.spider_cls.name)
        create_init(self.test_spider_dir)

    def gen_template(self):
        self._create_body()

    def _create_body(self):
        spider_name = self.spider_cls.__name__
        spider_module = self.spider_cls.__module__
        httpcache_dir = Settings().get('HTTPCACHE_DIR')

        parse_func_tmpls = []
        fixture_tmpls = []
        for parse_func in self.rsp_factory.result.keys():
            parse_func_tmpls.append(tmpl_parse_func.substitute(**{
                'spider_parse_func': parse_func,
                'spider': spider_name
            }).strip())
            fixture_tmpls.append(tmpl_fixture.substitute(**{
                'spider_parse_func': parse_func,
            }).strip())
        fixture = '\n\n\n'.join(fixture_tmpls)
        fixture_import = tmpl_fixture_import.substitute(**{
            'spider_module': spider_module,
            'spider': spider_name,
            'httpcache_dir': httpcache_dir
        }).strip()
        fixture_spider = tmpl_fixture_spider.substitute(**{
            'spider': spider_name
        }).strip()

        conftest = '\n\n\n'.join([fixture_import, fixture_spider, fixture])
        parse_func = '\n\n\n'.join(parse_func_tmpls)
        create_subfile(self.test_spider_dir, 'conftest', conftest + '\n')
        create_subfile(self.test_spider_dir, 'test_parse', parse_func + '\n')
