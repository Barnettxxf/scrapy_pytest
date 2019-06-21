pytest_plugins = ('scrapy_pytest.plugins.ymspider', )


def test_plugin(scrapy_plugin):
    assert scrapy_plugin == 'scrapy_plugin'
