"""
Author: xuxiongfeng
Date: 2019-06-13 17:57
Usage: 
"""

from scrapy.http import TextResponse, Response
from scrapy.responsetypes import responsetypes
from scrapy.utils.gz import gunzip

import zlib

from scrapy.utils.misc import load_object

from ..settings import Settings

ACCEPTED_ENCODINGS = [b'gzip', b'deflate']

try:
    import brotli

    ACCEPTED_ENCODINGS.append(b'br')
except ImportError:
    pass


class RetrieveResponse:
    def __init__(self, settings=None):
        if settings is None:
            settings = Settings()
        if isinstance(settings, dict):
            settings = Settings(settings)

        self.storage = load_object(settings['HTTPCACHE_STORAGE'])(settings)

    def retrieve_response(self, spider, request):
        response = self.storage.retrieve_response(spider, request)
        response.request = request
        return self.http_compression(response)

    def http_compression(self, response):
        if isinstance(response, Response):
            content_encoding = response.headers.getlist('Content-Encoding')
            if content_encoding:
                encoding = content_encoding.pop()
                decoded_body = self._decode(response.body, encoding.lower())
                respcls = responsetypes.from_args(headers=response.headers, url=response.url, body=decoded_body)
                kwargs = dict(cls=respcls, body=decoded_body)
                if issubclass(respcls, TextResponse):
                    kwargs['encoding'] = None
                response = response.replace(**kwargs)
                if not content_encoding:
                    del response.headers['Content-Encoding']

        return response

    def open(self, spider_cls):
        self.storage.open_spider(spider_cls)

    def close(self, spider_cls):
        self.storage.open_spider(spider_cls)

    def _decode(self, body, encoding):
        if encoding == b'gzip' or encoding == b'x-gzip':
            body = gunzip(body)

        if encoding == b'deflate':
            try:
                body = zlib.decompress(body)
            except zlib.error:
                body = zlib.decompress(body, -15)
        if encoding == b'br' and b'br' in ACCEPTED_ENCODINGS:
            body = brotli.decompress(body)
        return body
