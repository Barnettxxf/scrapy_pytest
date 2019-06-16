from scrapy_pytest.web.app import app
from scrapy_pytest.web.common import get_responses, save_data
from scrapy_pytest import env

app_ctx = app.app_context()
app_ctx.push()
from scrapy_pytest.web.models import ParseFunc, Reqeust, Spider, Storage

from cache_dir import cache_dir


def test_web_utils():
    env.set_httpcache_dir(cache_dir)
    with app.app_context():
        save_data()
        print(Reqeust.query.all())
    app_ctx.pop()
