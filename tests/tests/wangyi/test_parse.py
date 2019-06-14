def test_parse(parse_response, WangyiSpider):
    gen = WangyiSpider().parse(parse_response)
    for result in gen:
        # specified operation
        pass
