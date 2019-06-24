import six

HTTPCACHE_DIR = '/tmp/scrapy_httpcache'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_GZIP = False
HTTPCACHE_STORAGE = 'scrapy_pytest.storage.DbmCacheStorage'
HTTPCACHE_DBM_MODULE = 'anydbm' if six.PY2 else 'dbm'
HTTPCACHE_ALWAYS_STORE = False
HTTPCACHE_ENABLED = True
