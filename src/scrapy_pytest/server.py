import os

from .web.app import app
import click
from . import env


@click.command(help='Start httpcache server, so that you can scan all httpcache info you specified on web browser')
@click.option('--port', '-p', default=5000, help='web server port', type=int)
@click.option('--host', '-h', default='127.0.0.1', help='web server host', type=str)
@click.option('--httpcache', '-c', default='', help='httpcache dir')
def run(port, host, httpcache):
    if httpcache:
        env.set_httpcache_dir(httpcache)

    app.run(host=host, port=port)


@click.group()
def cli():
    pass


cli.add_command(run)
