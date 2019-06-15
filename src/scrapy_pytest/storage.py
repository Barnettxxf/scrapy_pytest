from __future__ import print_function
import os

from six.moves import cPickle as pickle
from time import time
from w3lib.http import headers_dict_to_raw
from scrapy.utils.python import to_bytes
from scrapy.extensions.httpcache import FilesystemCacheStorage as _FilesystemCacheStorage, \
    DbmCacheStorage as _DbmCacheStorage

from . import Settings
from .utils.request import request_to_dict


class FilesystemCacheStorage(_FilesystemCacheStorage):
    def __init__(self, settings=Settings()):
        super().__init__(settings)

    def store_response(self, spider, request, response):
        """Store the given response in the cache."""
        rpath = self._get_request_path(spider, request)
        if not os.path.exists(rpath):
            os.makedirs(rpath)
        metadata = {
            'url': request.url,
            'method': request.method,
            'status': response.status,
            'response_url': response.url,
            'timestamp': time(),
            'request': request_to_dict(request),  # add
            'spider': spider.name  # add
        }
        with self._open(os.path.join(rpath, 'meta'), 'wb') as f:
            f.write(to_bytes(repr(metadata)))
        with self._open(os.path.join(rpath, 'pickled_meta'), 'wb') as f:
            pickle.dump(metadata, f, protocol=2)
        with self._open(os.path.join(rpath, 'response_headers'), 'wb') as f:
            f.write(headers_dict_to_raw(response.headers))
        with self._open(os.path.join(rpath, 'response_body'), 'wb') as f:
            f.write(response.body)
        with self._open(os.path.join(rpath, 'request_headers'), 'wb') as f:
            f.write(headers_dict_to_raw(request.headers))
        with self._open(os.path.join(rpath, 'request_body'), 'wb') as f:
            f.write(request.body)

    def find_request_path(self, spider_cls):
        paths = []
        spider_httpcache_path = os.path.join(self.cachedir, spider_cls.name)
        for path in os.listdir(spider_httpcache_path):
            _path = os.path.join(spider_httpcache_path, path)
            if os.path.isdir(_path):
                for p in os.listdir(_path):
                    paths.append(os.path.join(_path, p))
        return paths

    def close(self):
        pass


class DbmCacheStorage(_DbmCacheStorage):
    def __init__(self, settings=Settings()):
        super().__init__(settings)

    def store_response(self, spider, request, response):
        key = self._request_key(request)
        data = {
            'status': response.status,
            'url': response.url,
            'headers': dict(response.headers),
            'body': response.body,
            'request': request_to_dict(request),  # add
            'spider': spider.name  # add
        }
        self.db['%s_data' % key] = pickle.dumps(data, protocol=2)
        self.db['%s_time' % key] = str(time())

    def find_request_path(self, spider_cls):
        raise NotImplementedError

    def close(self):
        self.db.close()


storage_class = {
    'filesystem': 'scrapy_pytest.storage.FilesystemCacheStorage',
    'dbm': 'scrapy_pytest.storage.DbmCacheStorage',
}
