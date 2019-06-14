def test_parse(parse_resposne, BaiduSpider):
    gen = BaiduSpider().parse(parse_resposne)
    for result in gen:
        # specified operation
        pass
