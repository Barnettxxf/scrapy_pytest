# automatically created by scrapy_pytest


def test_parse(parse_response, BaiduSpider):
    gen = BaiduSpider().parse(parse_response)
    for result in gen:
        # specified operation
        pass
