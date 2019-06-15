import six
from scrapy.settings import BaseSettings

from . import default_settings as default_settings_module


class Settings(BaseSettings):
    # prevent ~.__init__ from running twice
    _flag = True

    def __new__(cls, *args, **kwargs):
        if not hasattr(Settings, '_instance'):
            Settings._instance = object.__new__(cls)
        return Settings._instance

    def __init__(self, values=None, priority='project'):
        if not Settings._flag:
            return
        Settings._flag = False
        super().__init__()
        self.setmodule(default_settings_module, 'default')
        for name, val in six.iteritems(self):
            if isinstance(val, dict):
                self.set(name, BaseSettings(val, 'default'), 'default')
        self.update(values, priority)
