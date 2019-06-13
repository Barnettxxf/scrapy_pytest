from scrapy.extensions.httpcache import FilesystemCacheStorage as _FilesystemCacheStorage, \
    DbmCacheStorage as _DbmCacheStorage


class FilesystemCacheStorage(_FilesystemCacheStorage):
    pass


class DbmCacheStorage(_DbmCacheStorage):
    pass
