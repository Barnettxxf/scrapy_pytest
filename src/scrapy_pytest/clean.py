import os
from shutil import rmtree
from scrapy.utils.request import request_fingerprint

from .filter import RequestFilter
from . import env


def get_target_dir(cond, rfilter, spider_httpcache_path):
    for req in rfilter[cond]:
        key = request_fingerprint(req)
        rpath = os.path.join(spider_httpcache_path, key[0:2], key)
        yield rpath


def get_all_spider_httpcache(spider_httpcache_path):
    paths = []
    for path in os.listdir(spider_httpcache_path):
        _path = os.path.join(spider_httpcache_path, path)
        if os.path.isdir(_path):
            for p in os.listdir(_path):
                paths.append(os.path.join(_path, p))
    return paths


def remove(rpath):
    print('try to remove %s' % rpath)
    try:
        rmtree(rpath)
    except Exception as e:
        print('remove failed', ','.join(e.args))


def clean_no_need_cache(spider_cls, conditions=None, except_conditions=None, settings=None):
    spider_httpcache_path = os.path.join(env.get_httpcache_dir(), spider_cls.name)

    rfilter = RequestFilter(spider_cls, settings)
    if conditions:
        for cond in conditions:
            for rpath in get_target_dir(cond, rfilter, spider_httpcache_path):
                remove(rpath)

    elif except_conditions:
        not_remove_dir = []
        for cond in except_conditions:
            for rpath in get_target_dir(cond, rfilter, spider_httpcache_path):
                not_remove_dir.append(rpath)
        all_httpcache_dir = get_all_spider_httpcache(spider_httpcache_path)
        for httpcache_dir in all_httpcache_dir:
            if httpcache_dir not in not_remove_dir:
                remove(httpcache_dir)
    else:
        raise ValueError('Must be set condition or except_conditions')
