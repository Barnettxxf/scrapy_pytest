import scrapy


def mock_parse():
    def _mock_parse(self, response):
        pass

    return _mock_parse


def mock_spidercls():
    class MockSpider(scrapy.Spider):
        name = 'mock'

        def parse(self, response):
            pass

    return MockSpider


def get_spidercls_with_mock_parse(spider_name, parsefunc_names):
    _mock_spidercls = mock_spidercls()
    setattr(_mock_spidercls, 'name', spider_name)

    for parsefunc_name in parsefunc_names:
        _mock_parse_func = mock_parse()
        _mock_parse_func.__name__ = parsefunc_name
        setattr(_mock_spidercls, parsefunc_name, _mock_parse_func)

    return _mock_spidercls
