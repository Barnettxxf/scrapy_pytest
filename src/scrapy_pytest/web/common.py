import os
from collections import defaultdict

from ..mock import mock_spidercls
from ..factory import ResponseFactory
from ..storage import storage_class
from .. import env


def find_spiders():
    httpcache_dir = env.get_httpcache_dir()
    spider_names = {
        'filesystem': set(),
        'dbm': set(),
    }
    for name in os.listdir(httpcache_dir):
        abs_path = os.path.join(httpcache_dir, name)
        if os.path.isdir(abs_path):
            spider_names['filesystem'].add(name)
        elif '.db.' in name:
            spider_names['dbm'].add(name.split('.', maxsplit=1)[0])
    return spider_names


def mock_spiders():
    spidercls = defaultdict(list)
    for storage, spider_names in find_spiders().items():
        for spider_name in spider_names:
            _spidercls = mock_spidercls()
            setattr(_spidercls, 'name', spider_name)
            spidercls[storage].append(_spidercls)
    return spidercls


def get_responses():
    responses = defaultdict(dict)
    for storage, spiderclss in mock_spiders().items():
        env.set_httpcache_storage(storage_class[storage])
        for spidercls in spiderclss:
            rsp_factory = ResponseFactory(spidercls)
            responses[storage][spidercls.name] = rsp_factory.result
    return responses
