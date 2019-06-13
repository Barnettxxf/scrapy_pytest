"""
Author: xuxiongfeng
Date: 2019-06-13 16:52
Usage: 
"""
from __future__ import print_function
from time import time
from weakref import WeakKeyDictionary

from scrapy.extensions.httpcache import parse_cachecontrol
from scrapy.http import Response
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes


class RFC2616Policy(object):
    MAXAGE = 3600 * 24 * 365  # one year

    def __init__(self, settings):
        self.always_store = settings.getbool('HTTPCACHE_ALWAYS_STORE')
        self.ignore_schemes = settings.getlist('HTTPCACHE_IGNORE_SCHEMES')
        self.ignore_response_cache_controls = [to_bytes(cc) for cc in
                                               settings.getlist('HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS')]
        self._cc_parsed = WeakKeyDictionary()

    def _parse_cachecontrol(self, r):
        if r not in self._cc_parsed:
            cch = r.headers.get(b'Cache-Control', b'')
            parsed = parse_cachecontrol(cch)
            if isinstance(r, Response):
                for key in self.ignore_response_cache_controls:
                    parsed.pop(key, None)
            self._cc_parsed[r] = parsed
        return self._cc_parsed[r]

    def should_cache_request(self, request):
        if urlparse_cached(request).scheme in self.ignore_schemes:
            return False
        cc = self._parse_cachecontrol(request)
        # obey user-agent directive "Cache-Control: no-store"
        if b'no-store' in cc:
            return False
        # Any other is eligible for caching
        return True

    def should_cache_response(self, response, request):
        # What is cacheable - https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec14.9.1
        # Response cacheability - https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.4
        # Status code 206 is not included because cache can not deal with partial contents
        cc = self._parse_cachecontrol(response)
        # obey directive "Cache-Control: no-store"
        if b'no-store' in cc:
            return False
        # Never cache 304 (Not Modified) responses
        elif response.status == 304:
            return False
        # Cache unconditionally if configured to do so
        elif self.always_store:
            return True
        # Any hint on response expiration is good
        elif b'max-age' in cc or b'Expires' in response.headers:
            return True
        # Firefox fallbacks this statuses to one year expiration if none is set
        elif response.status in (300, 301, 308):
            return True
        # Other statuses without expiration requires at least one validator
        elif response.status in (200, 203, 401):
            return b'Last-Modified' in response.headers or b'ETag' in response.headers
        # Any other is probably not eligible for caching
        # Makes no sense to cache responses that does not contain expiration
        # info and can not be revalidated
        else:
            return False

    def is_cached_response_fresh(self, cachedresponse, request):
        cc = self._parse_cachecontrol(cachedresponse)
        ccreq = self._parse_cachecontrol(request)
        if b'no-cache' in cc or b'no-cache' in ccreq:
            return False

        now = time()
        freshnesslifetime = self._compute_freshness_lifetime(cachedresponse, request, now)
        currentage = self._compute_current_age(cachedresponse, request, now)

        reqmaxage = self._get_max_age(ccreq)
        if reqmaxage is not None:
            freshnesslifetime = min(freshnesslifetime, reqmaxage)

        if currentage < freshnesslifetime:
            return True

        if b'max-stale' in ccreq and b'must-revalidate' not in cc:
            # From RFC2616: "Indicates that the client is willing to
            # accept a response that has exceeded its expiration time.
            # If max-stale is assigned a value, then the client is
            # willing to accept a response that has exceeded its
            # expiration time by no more than the specified number of
            # seconds. If no value is assigned to max-stale, then the
            # client is willing to accept a stale response of any age."
            staleage = ccreq[b'max-stale']
            if staleage is None:
                return True

            try:
                if currentage < freshnesslifetime + max(0, int(staleage)):
                    return True
            except ValueError:
                pass

        # Cached response is stale, try to set validators if any
        self._set_conditional_validators(request, cachedresponse)
        return False

    def is_cached_response_valid(self, cachedresponse, response, request):
        # Use the cached response if the new response is a server error,
        # as long as the old response didn't specify must-revalidate.
        if response.status >= 500:
            cc = self._parse_cachecontrol(cachedresponse)
            if b'must-revalidate' not in cc:
                return True

        # Use the cached response if the server says it hasn't changed.
        return response.status == 304

    def _set_conditional_validators(self, request, cachedresponse):
        if b'Last-Modified' in cachedresponse.headers:
            request.headers[b'If-Modified-Since'] = cachedresponse.headers[b'Last-Modified']

        if b'ETag' in cachedresponse.headers:
            request.headers[b'If-None-Match'] = cachedresponse.headers[b'ETag']

    def _get_max_age(self, cc):
        try:
            return max(0, int(cc[b'max-age']))
        except (KeyError, ValueError):
            return None

    def _compute_freshness_lifetime(self, response, request, now):
        # Reference nsHttpResponseHead::ComputeFreshnessLifetime
        # https://dxr.mozilla.org/mozilla-central/source/netwerk/protocol/http/nsHttpResponseHead.cpp#706
        cc = self._parse_cachecontrol(response)
        maxage = self._get_max_age(cc)
        if maxage is not None:
            return maxage

        # Parse date header or synthesize it if none exists
        date = rfc1123_to_epoch(response.headers.get(b'Date')) or now

        # Try HTTP/1.0 Expires header
        if b'Expires' in response.headers:
            expires = rfc1123_to_epoch(response.headers[b'Expires'])
            # When parsing Expires header fails RFC 2616 section 14.21 says we
            # should treat this as an expiration time in the past.
            return max(0, expires - date) if expires else 0

        # Fallback to heuristic using last-modified header
        # This is not in RFC but on Firefox caching implementation
        lastmodified = rfc1123_to_epoch(response.headers.get(b'Last-Modified'))
        if lastmodified and lastmodified <= date:
            return (date - lastmodified) / 10

        # This request can be cached indefinitely
        if response.status in (300, 301, 308):
            return self.MAXAGE

        # Insufficient information to compute fresshness lifetime
        return 0

    def _compute_current_age(self, response, request, now):
        # Reference nsHttpResponseHead::ComputeCurrentAge
        # https://dxr.mozilla.org/mozilla-central/source/netwerk/protocol/http/nsHttpResponseHead.cpp#658
        currentage = 0
        # If Date header is not set we assume it is a fast connection, and
        # clock is in sync with the server
        date = rfc1123_to_epoch(response.headers.get(b'Date')) or now
        if now > date:
            currentage = now - date

        if b'Age' in response.headers:
            try:
                age = int(response.headers[b'Age'])
                currentage = max(currentage, age)
            except ValueError:
                pass

        return currentage
