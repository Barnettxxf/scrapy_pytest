import os
from .settings import settings


def get_httpcache_dir():
    return settings.get('HTTPCACHE_DIR', None)


def set_httpcache_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    settings.update({
        'HTTPCACHE_DIR': path
    })
