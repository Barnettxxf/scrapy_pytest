"""
Author: xuxiongfeng
Date: 2019-06-14 10:42
Usage: 
"""
from scrapy import Request, FormRequest


def request_to_dict(request):
    metadata = {}
    for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', 'flags',
              'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
        metadata[x] = getattr(request, x)
    metadata['cls'] = type(request).__name__
    return metadata


def request_from_dict(metadata):
    request = Request(url=metadata['request']['url'])
    metadata['request']['cls'] = eval(metadata['request']['cls'])
    return request.replace(**metadata)
