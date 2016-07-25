import os
import click
from mssapi.s3.connection import S3Connection


class MssClient:
    def __init__(self, host="mtmss.com", port=80):
        self.access_key = os.environ.get('MSS_KEY')
        self.access_secret = os.environ.get('MSS_SECRET')
        self.host = host
        self.port = port
        self.conn = S3Connection(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.access_secret,
            port=port,
            host=host,
        )

    def upload_file(self, bucket, expires_in, file_name):
        if not bucket in self.conn:
            b = self.conn.create_bucket(bucket)
        else:
            b = self.conn.get_bucket(bucket)
        k = b.new_key(file_name)
        k.set_contents_from_filename(file_name)
        return k.generate_url(expires_in)


@click.command()
@click.option('-b', '--bucket', default="mssup", help='butket name')
@click.option('-t', '--expires_in', default=31536000, help='expire time')
@click.argument('file_name')
def main(bucket, expires_in, file_name):
    """
    A simple tool to upload file to meituan object bucket.
    Please set environment variables MSS_KEY and MSS_SECRET first.
    """
    c = MssClient()
    url = c.upload_file(bucket, expires_in, file_name)
    click.echo(url)


if __name__ == '__main__':
    main()
