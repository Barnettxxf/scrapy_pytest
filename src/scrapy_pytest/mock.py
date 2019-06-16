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
