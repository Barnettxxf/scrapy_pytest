from scrapy.settings import Settings

from . import default_settings

settings = Settings({k: v for k, v in vars(default_settings).items() if k.isupper()})
