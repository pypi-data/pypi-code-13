import click
from lxml import html
import requests
import os

DATA_DIR = './data/'

@click.command()
@click.argument('url', type=click.STRING, default='https://en.wikipedia.org/wiki/Mathematics')
@click.argument('name', type=click.STRING, default='')
def main(url, name):
    print "Pointing to %s" % url
    print "Downloading %s" % url
    page = requests.get(url)
    tree = html.fromstring(page.content)
    print "Downloaded %s" % url
    if name == '':
        name = os.path.join(DATA_DIR,url.split('/')[-1])

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    with open(name, 'w') as f:
        f.write(page.content)

    print "WE MADE IT :D"



if __name__ == '__main__':
    main()
