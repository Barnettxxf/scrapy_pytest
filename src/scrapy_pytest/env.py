import os
from .settings import Settings

settings = Settings()


def update(name, value):
    settings.update(
        {name: value}, priority='spider'
    )


def get(name, default=None):
    return settings.get(name, default)


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
    return settings.keys()


def values():
    return settings.values()


def items():
    return settings.items()


def set_always_store_httpcache():
    update('HTTPCACHE_ALWAYS_STORE', True)


def cancel_always_store_httpcache():
    update('HTTPCACHE_ALWAYS_STORE', False)
