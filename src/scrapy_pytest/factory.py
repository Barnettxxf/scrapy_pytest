import os
from collections import defaultdict

from scrapy.utils.misc import load_object
import pickle

from .utils.templates import create_subfile, tmpl_fixture, tmpl_fixture_import, \
    tmpl_parse_func, tmpl_fixture_spider, create_init
from . import RetrieveResponse, env
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

        self._requests = defaultdict(list)
        self.storage = load_object(self.settings['HTTPCACHE_STORAGE'])(self.settings)
        self.storage.open_spider(spider_cls)

    def _gen_request(self):
        for rpath in self.storage.find_request_path(self.spider_cls):
            metadata = self.storage.read_meta(rpath)
            yield request_from_dict(metadata, self.spider_cls)

    def _read_meta(self, rpath):
        metapath = os.path.join(rpath, 'pickled_meta')
        if not os.path.exists(metapath):
            return  # not found
        with open(metapath, 'rb') as f:
            return pickle.load(f)

    @property
    def reqs(self):
        if len(self._requests) == 0:
            for req in self._gen_request():
                callback = req.callback or self.spider_cls.parse
                self._requests[callback.__name__].append(req)

        return self._requests

    def close(self):
        self.storage.close_spider(self.spider_cls)


class ResponseFactory:
    def __init__(self, spider_cls, settings=None):
        self.req_factory = RequestFactory(spider_cls, settings)
        self.spider_cls = spider_cls

        self.storage = RetrieveResponse(settings or self.req_factory.settings)
        self.storage.open(self.spider_cls)

        self.filter_set = set()
        self._result = defaultdict(list)

    def gen(self):
        for parse_func, reqs in self.req_factory.reqs.items():
            rsps = [self.storage.retrieve_response(self.spider_cls, req) for req in reqs]
            yield parse_func, rsps

    @property
    def result(self):
        if len(self._result) == 0:
            for parse_func, rsps in self.gen():
                self._result[parse_func].extend(rsps)
        return self._result

    def close(self):
        self.req_factory.close()
        self.storage.close(self.spider_cls)


class TemplateFactory:
    def __init__(self, spider_cls, project_dir=None, settings=Settings(), test_dir_name='tests'):
        self.rsp_factory = ResponseFactory(spider_cls, settings)
        self.project_dir = project_dir or os.getcwd()
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
        httpcache_dir = env.get_httpcache_dir()

        parse_func_tmpls = []
        parse_func_tmpls.append('# automatically created by scrapy_pytest')
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
            'httpcache_dir': httpcache_dir,
            'storage': env.get_httpcache_storage()
        }).strip()
        fixture_spider = tmpl_fixture_spider.substitute(**{
            'spider': spider_name
        }).strip()
        conftest = '\n\n\n'.join([fixture_import, fixture_spider, fixture])
        parse_func = '\n\n\n'.join(parse_func_tmpls)
        create_subfile(self.test_spider_dir, 'conftest', conftest + '\n')
        create_subfile(self.test_spider_dir, 'test_parse', parse_func + '\n')

    def __del__(self):
        self.rsp_factory.close()
