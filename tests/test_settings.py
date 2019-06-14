"""
Author: xuxiongfeng
Date: 2019-06-14 14:10
Usage: 
"""

from scrapy_pytest.settings import Settings


def test_settings_singleton():
    assert Settings() == Settings(), "Not the same instance"
