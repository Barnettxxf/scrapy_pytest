import os
from string import Template

tmpl_plugins_file_header = Template("""
pytest_plugins = (${plugins})
""")

tmpl_plugin = Template("""
'scrapy_pytest.plugins.${plugin}'
""")

tmpl_fixture = Template("""
@pytest.fixture(scope="module", params=rsp_factory.result['${spider_parse_func}'])
def ${spider_parse_func}_response(empty, request):
    if isinstance(request.param, (tuple, list)):
        response = request.param[0]
    else:
        response = request.param
    return response
""")

tmpl_fixture_import = Template("""
# automatically created by scrapy_pytest


import pytest
from scrapy_pytest import factory, env
from ${spider_module} import ${spider} as _${spider}

env.set_httpcache_dir('${httpcache_dir}')
env.set_httpcache_storage('${storage}')

rsp_factory = factory.ResponseFactory(_${spider})

    
@pytest.fixture(scope='session')
def empty(request):
    request.addfinalizer(rsp_factory.close)
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
