import click
import knowlify
from lxml import html
import requests
import os
import config
import time


@click.command()
@click.argument('filename_or_url', type=click.STRING, default='https://en.wikipedia.org/wiki/Mathematics')
@click.option('-p','path', type=click.STRING, default=None)
def main(filename_or_url, path):
    page = knowlify.get_page(filename_or_url)
    return knowlify.output_page(page, path)


if __name__ == '__main__':
    main()
