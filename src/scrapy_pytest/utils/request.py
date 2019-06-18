import six
from scrapy import Request, FormRequest
from ..mock import mock_spidercls, mock_parse


def request_to_dict(request) -> dict:
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


def request_from_dict(metadata, spider_cls) -> Request:
    request = Request(url=metadata['request']['url'])
    for x in metadata['request']:
        if x in ['callback', 'errback']:
            if metadata['request'][x] is not None:
                if spider_cls.__name__ == mock_spidercls().__name__ and metadata['request'][x] != 'parse':
                    _mock_parse = mock_parse()
                    _mock_parse.__name__ = metadata['request'][x]
                    setattr(spider_cls, metadata['request'][x], _mock_parse)
                metadata['request'][x] = getattr(spider_cls, metadata['request'][x])
    metadata['request']['cls'] = eval(metadata['request']['cls']) if six.string_types else metadata['request']['cls']
    return request.replace(**metadata['request'])
