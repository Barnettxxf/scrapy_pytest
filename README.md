## Scrapy-Pytest
Scrapy-Pytest，是基于`pytest`的方便为`Scrapy`框架写的爬虫设计的单元测试工具。其主要基于`Scrapy`的`HTTPCache`
功能缓存的`Request`和`Response`数据，通过`HTTP`缓存，生产对应的`Request`和`Response`对象，可以不重新依赖
于网络进行对`Scrapy`爬虫的测试，目前可以支持自动生产`Scrapy`爬虫的各个解析函数（内置`parse`或自定义）单元测试文件，
模版，以及简单的`HTTP`缓存的`Web Server`管理功能


### Install
以下提供两种方式：
1. 在项目根目录中执行以下命令即可
```bash
pip install -e git+https://github.com/Barnettxxf/scrapy_pytest#egg=scrapy_pytest
```

 该方法会在项目根目录上自动创建`src`文件并将本项目代码克隆到`src`文件夹中作为`library root`
2. 将本项目克隆到本地，切换至其文件夹中，在用`pip`安装
```bash
git clone https://github.com/Barnettxxf/scrapy_pytest.git
cd scrapy_pytest && pip install .
```
 该方法会将scrapy_pytest作为第三方包放置在对应`python`环境的`site-packages`文件夹下

### Usage
1. 定义`HTTP`缓存的目录
```python
# content of cache_dir.py 和spiders同一级目录
import os

cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
```
2. `Scrapy`爬虫例子, 并运行，将`HTTP`缓存下来，供后面测试使用
```python
# part content of spiders/wangyi.py, you can see all in tests/spiders/wangyi.py
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_pytest import storage_class

from cache_dir import cache_dir


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'

    def start_requests(self):
        ...

    def parse(self, response):
        ...

    def parse_detail(self, response):
        ...


if __name__ == '__main__':
    settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': cache_dir,
        'HTTPCACHE_STORAGE': storage_class['filesystem']
    }
    cp = CrawlerProcess(settings=settings)
    cp.crawl(WangyiSpider)
    cp.start()
```

3. 编写单元测试模版生成脚本，使用`scrapy_pytest`生成基于`pytest`的单元测试文件
```python
# content of template_factory.py
from scrapy_pytest.factory import TemplateFactory
from scrapy_pytest import env
from spiders import WangyiSpider
from cache_dir import cache_dir

env.set_httpcache_dir(cache_dir) # tell your httpcache dir location


tmpl_factory = TemplateFactory(WangyiSpider, test_dir_name='auto_gen_tests')
tmpl_factory.gen_template()
```
运行后将会得到类似的文件目录
```
cache_dir.py

template_factory.py
    # content .. see above

spiders/
    wangyi.py
        # content ... see above 

auto_gen_tests/  # automaically generated by template_factory.py
    __init__.py
    
    wangyi/
        __init__.py
        
        conftest.py
            # content of tests/tests/wangyi/contest.py
            # automatically created by scrapy_pytest
            
            
            import pytest
            from scrapy_pytest import factory, env
            from tests.spiders.Wangyi import WangyiSpider as _WangyiSpider
            
            ... # you can see all in tests/auto_gen_tests/wangyi/conftest.py
            
            @pytest.fixture(scope="module", params=rsp_factory.result['parse_detail'])
            def parse_detail_response(empty, request):
                if isinstance(request.param, (tuple, list)):
                    response = request.param[0]
                else:
                    response = request.param
                return response
        
        test_parse.py
            # content of tests/tests/wangyi/contest.py
            # automatically created by scrapy_pytest


            def test_parse(parse_response, WangyiSpider):
                gen = WangyiSpider().parse(parse_response)
                for result in gen:
                    # specified operation
                    pass
            
            ... # you can see all in tests/auto_gen_tests/wangyi/test_parse.py

cache/
    # httpcache dir
    ...
```

### Web Server
...

### TODO
...


