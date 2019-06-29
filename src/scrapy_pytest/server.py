import os

from .web.app import app
import click
from . import env


@click.command(help='Start httpcache server, so that you can scan all httpcache info you specified on web browser')
@click.option('--port', '-p', default=5000, help='web server port', type=int)
@click.option('--host', '-h', default='127.0.0.1', help='web server host', type=str)
@click.option('--httpcache', '-c', default='', help='httpcache dir')
@click.option('--init-db', is_flag=True, default=False, help='whether init db or not, default not')
def run(port, host, httpcache, init_db):
    _httpcache = httpcache or search_current_dir()
    if _httpcache:
        env.set_httpcache_dir(_httpcache)
        app.logger.info('set httpcache dir: %s', _httpcache)

    if init_db:
        from .web.exts import db
        with app.app_context():
            db.drop_all()
            db.create_all()
        app.logger.info('reinit database.')

    app.run(host=host, port=port)


def search_current_dir():
    _current_cache = os.path.join(os.getcwd(), 'cache')
    if not os.path.exists(_current_cache):
        return
    return _current_cache


@click.command('init-db', help='init database from httpcache_dir, which will generate a sqlite database file')
@click.option('--httpcache', '-c', default='', help='httpcache dir')
def init_db(httpcache):
    _httpcache = httpcache or search_current_dir()
    if _httpcache:
        env.set_httpcache_dir(_httpcache)
        print('set httpcache dir:', _httpcache)

    from .web.exts import db
    with app.app_context():
        app.logger.info('delete all data')
        db.drop_all()
        app.logger.info('write httpcache data to database')
        db.create_all()


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(init_db)
