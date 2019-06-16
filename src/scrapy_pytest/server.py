from .web.app import app
import click
from . import env


@click.command(help='Start httpcache server, so that you can scan all httpcache info you specified on web browser')
@click.option('--httpcache', '-c', default='', help='httpcache dir')
def run(httpcache):
    if httpcache:
        env.set_httpcache_dir(httpcache)
    app.run()


@click.group()
def cli():
    pass


cli.add_command(run)
