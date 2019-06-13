"""
Author: xuxiongfeng
Date: 2019-06-13 17:51
Usage: 
"""
import pytest
import scrapy


@pytest.fixture
def response():
    request = scrapy.Request(url='https://www.baidu.com')

