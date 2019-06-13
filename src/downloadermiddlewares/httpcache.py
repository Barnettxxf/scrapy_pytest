"""
Author: xuxiongfeng
Date: 2019-06-13 16:47
Usage: 
"""

from email.utils import formatdate
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.misc import load_object


class HttpCacheMiddleware(object):
    DOWNLOAD_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError)

    def __init__(self, settings):
        self.policy = load_object(settings['HTTPCACHE_POLICY'])(settings)
        self.storage = load_object(settings['HTTPCACHE_STORAGE'])(settings)
        self.ignore_missing = settings.getbool('HTTPCACHE_IGNORE_MISSING')

    def spider_opened(self, spider):
        self.storage.open_spider(spider)

    def spider_closed(self, spider):
        self.storage.close_spider(spider)

    def process_request(self, request, spider):
        if request.meta.get('dont_cache', False):
            return

        # Skip uncacheable requests
        if not self.policy.should_cache_request(request):
            request.meta['_dont_cache'] = True  # flag as uncacheable
            return

        # Look for cached response and check if expired
        cachedresponse = self.storage.retrieve_response(spider, request)
        if cachedresponse is None:
            if self.ignore_missing:
                raise IgnoreRequest("Ignored request not in cache: %s" % request)
            return  # first time request

        # Return cached response only if not expired
        cachedresponse.flags.append('cached')
        if self.policy.is_cached_response_fresh(cachedresponse, request):
            return cachedresponse

        # Keep a reference to cached response to avoid a second cache lookup on
        # process_response hook
        request.meta['cached_response'] = cachedresponse

    def process_response(self, request, response, spider):
        if request.meta.get('dont_cache', False):
            return response

        # Skip cached responses and uncacheable requests
        if 'cached' in response.flags or '_dont_cache' in request.meta:
            request.meta.pop('_dont_cache', None)
            return response

        # RFC2616 requires origin server to set Date header,
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.18
        if 'Date' not in response.headers:
            response.headers['Date'] = formatdate(usegmt=1)

        # Do not validate first-hand responses
        cachedresponse = request.meta.pop('cached_response', None)
        if cachedresponse is None:
            self._cache_response(spider, response, request, cachedresponse)
            return response

        if self.policy.is_cached_response_valid(cachedresponse, response, request):
            return cachedresponse

        self._cache_response(spider, response, request, cachedresponse)
        return response

    def process_exception(self, request, exception, spider):
        cachedresponse = request.meta.pop('cached_response', None)
        if cachedresponse is not None and isinstance(exception, self.DOWNLOAD_EXCEPTIONS):
            return cachedresponse

    def _cache_response(self, spider, response, request, cachedresponse):
        if self.policy.should_cache_response(response, request):
            self.storage.store_response(spider, request, response)
