import six
from scrapy.settings import BaseSettings

from . import default_settings as default_settings_module


class Settings(BaseSettings):

    def __new__(cls, *args, **kwargs):
        if not hasattr(Settings, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, values=None, priority='project'):
        super().__init__()
        self.setmodule(default_settings_module, 'default')
        for name, val in six.iteritems(self):
            if isinstance(val, dict):
                self.set(name, BaseSettings(val, 'default'), 'default')
        self.update(values, priority)
