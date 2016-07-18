from __future__ import absolute_import  # 2-3 compat

import click

from hark.lib.platform import cpu_cores
from hark_imagestore.server import ImagestoreServer
from hark_imagestore.imagecache import S3ImageCache

DEFAULT_WORKERS = (cpu_cores() * 2) + 1


@click.command()
@click.option('--port', type=int, default=9000)
@click.option('--workers', type=int, default=DEFAULT_WORKERS)
@click.option('--local', is_flag=True, default=False)
@click.option('--hark-home', envvar='HARKHOME', type=str, default=None)
@click.option(
    '--aws-access-key-id',
    envvar='AWS_ACCESS_KEY_ID', type=str, default=None)
@click.option(
    '--aws-secret-access-key',
    envvar='AWS_SECRET_ACCESS_KEY', type=str, default=None)
def hark_imagestore(
           port, workers, local, hark_home,
           aws_access_key_id, aws_secret_access_key):

    image_cache = S3ImageCache(aws_access_key_id, aws_secret_access_key)

    click.secho(
        "Starting gunicorn app on port %d with %d workers" %
        (port, workers), fg='green')

    srv = ImagestoreServer(image_cache, port, workers)
    srv.run()
