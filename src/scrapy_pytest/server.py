from .web.app import app
import click
from . import env


@click.command(help='Start httpcache server, so that you can scan all httpcache info you specified on web browser')
@click.option('--port', '-p', default=5000, help='web server port', type=int)
@click.option('--host', '-h', default='127.0.0.1', help='web server host', type=str)
@click.option('--httpcache', '-c', default='', help='httpcache dir')
@click.option('--init_db', default=False, type=bool, help='whether init db or not, default not')
def run(port, host, httpcache, init_db):
    if httpcache:
        env.set_httpcache_dir(httpcache)

    if init_db:
        from .web.exts import db
        with app.app_context():
            db.drop_all()
            db.create_all()

    app.run(host=host, port=port)


@click.command(help='init database from httpcache_dir, which will generate a sqlite database file')
@click.option('--httpcache', '-c', default='', help='httpcache dir')
def init_db(httpcache):
    if httpcache:
        env.set_httpcache_dir(httpcache)

    from .web.exts import db
    with app.app_context():
        db.drop_all()
        db.create_all()


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(init_db)
