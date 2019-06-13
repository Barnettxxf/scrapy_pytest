"""
Author: xuxiongfeng
Date: 2019-06-13 17:48
Usage: 
"""
import os

from tests.spiders.baidu import HTTPCACHE_DIR

os.environ['SCRAPY_HTTPCACHE_DIR'] = HTTPCACHE_DIR