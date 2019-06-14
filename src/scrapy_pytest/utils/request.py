"""
Author: xuxiongfeng
Date: 2019-06-14 10:42
Usage: 
"""
import six
from scrapy import Request, FormRequest


def request_to_dict(request):
    metadata = {}
    for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', 'flags',
              'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
        if x in ['callback', 'errback']:
            func = getattr(request, x)
            if func:
                metadata[x] = func.__name__
            else:
                metadata[x] = None
        else:
            metadata[x] = getattr(request, x)
    metadata['cls'] = type(request).__name__
    return metadata


def request_from_dict(metadata, spider_cls):
    request = Request(url=metadata['request']['url'])
    for x in metadata['request']:
        if x in ['callback', 'errback']:
            if metadata['request'][x] is not None:
                metadata['request'][x] = getattr(spider_cls(), metadata['request'][x])
    metadata['request']['cls'] = eval(metadata['request']['cls']) if six.string_types else metadata['request']['cls']
    return request.replace(**metadata['request'])
