"""
Author: xuxiongfeng
Date: 2019-06-14 16:27
Usage: 
"""
import os
from string import Template

tmpl_fixture = Template("""
@pytest.fixture
def ${spider_parse_func}_response():
    return rsp_factory.result['${spider_parse_func}']
""")

tmpl_fixture_import = Template("""
import pytest
from scrapy_pytest import factory, env
from ${spider_module} import ${spider} as _${spider}

env.set_httpcache_dir('${httpcache_dir}')

rsp_factory = factory.ResponseFactory(_${spider})
""")

tmpl_fixture_spider = Template("""
@pytest.fixture
def ${spider}():
    return _${spider}
""")

tmpl_parse_func = Template("""
def test_${spider_parse_func}(${spider_parse_func}_response, ${spider}):
    gen = ${spider}().${spider_parse_func}(${spider_parse_func}_response)
    for result in gen:
        # specified operation
        pass
""")


def create_init(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with open(os.path.join(target_dir, '__init__.py'), 'w', encoding='utf-8'):
        pass


def create_subfile(target_dir, filename, body):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with open(os.path.join(target_dir, filename + '.py'), 'w', encoding='utf-8') as f:
        f.write(body)
