import six
from scrapy.settings import BaseSettings

from . import default_settings


class Settings(BaseSettings):
    """
    This object stores Scrapy settings for the configuration of internal
    components, and can be used for any further customization.

    It is a direct subclass and supports all methods of
    :class:`~scrapy.settings.BaseSettings`. Additionally, after instantiation
    of this class, the new object will have the global default settings
    described on :ref:`topics-settings-ref` already populated.
    """

    def __init__(self, values=None, priority='project'):
        # Do not pass kwarg values here. We don't want to promote user-defined
        # dicts, and we want to update, not replace, default dicts with the
        # values given by the user
        super(Settings, self).__init__()
        self.setmodule(default_settings, 'default')
        # Promote default dictionaries to BaseSettings instances for per-key
        # priorities
        for name, val in six.iteritems(self):
            if isinstance(val, dict):
                self.set(name, BaseSettings(val, 'default'), 'default')
        self.update(values, priority)

