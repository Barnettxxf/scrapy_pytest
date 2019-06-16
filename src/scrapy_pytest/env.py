import os
from .settings import Settings

default_settings = Settings()


def update(name, value):
    default_settings.update(
        {name: value}, priority='spider'
    )


def get(name, default=None):
    return default_settings.get(name, default)


def get_httpcache_dir():
    return get('HTTPCACHE_DIR')


def set_httpcache_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    update('HTTPCACHE_DIR', path)


def set_httpcache_storage(storage):
    update('HTTPCACHE_STORAGE', storage)


def get_httpcache_storage():
    return get('HTTPCACHE_STORAGE')


def keys():
    return default_settings.keys()


def values():
    return default_settings.values()


def items():
    return default_settings.items()
