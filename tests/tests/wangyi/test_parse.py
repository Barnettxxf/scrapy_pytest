# automatically created by scrapy_pytest


def test_parse_detail(parse_detail_response, WangyiSpider):
    gen = WangyiSpider().parse_detail(parse_detail_response)
    for result in gen:
        # specified operation
        pass


def test_parse(parse_response, WangyiSpider):
    gen = WangyiSpider().parse(parse_response)
    for result in gen:
        # specified operation
        pass
