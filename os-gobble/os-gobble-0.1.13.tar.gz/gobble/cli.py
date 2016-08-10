"""Command line interface for Gobble"""

import io

from json import loads
from click import command, argument, Path, group, option, echo
from os.path import join

from gobble.user import create_user
from gobble.fiscal import FiscalDataPackage
from gobble.config import ROOT_DIR
from gobble.search import search


@group()
def gobble():
    pass


@command()
def version():
    filename = join(ROOT_DIR, 'package.json')
    with io.open(filename) as json:
        package = loads(json.read())
        echo(package['version'])


@command()
def start():
    create_user()


@command()
@argument('filepath',
          type=Path(exists=True),
          metavar='full path to JSON datapackage descriptor')
def check(filepath):
    package = FiscalDataPackage(filepath)
    package.validate(raise_error=False)


@command()
@argument('query_all', required=False)
@option('--private', default=True, help='include private packages')
@option('--limit', default=50, help='limit the search results')
@option('--title', default=None, help='search package titles')
@option('--author', default=None, help='search packages by authors')
@option('--description', default=None, help='search packages by descriptions')
@option('--region', default=None, help='search packages by regions')
@option('--country', default=None, help='search packages by 2-digit country code')
@option('--city', default=None, help='search packages by city')
@option('--any', default=None, help='search packages by city')
def pull(private,
         limit,
         query_all,
         title,
         author,
         description,
         region,
         country,
         city):

    search_options = (
        ('title', title),
        ('author', author),
        ('description', description),
        ('regionCode', region),
        ('countryCode', country),
        ('cityCode', city)
    )

    if query_all:
        query = {'q': all}
    else:
        query = {key: value for key, value in search_options if value}

    search(query, private=private, limit=limit)


@command()
@argument('filepath', type=Path(exists=True))
def push(filepath):
    package = FiscalDataPackage(filepath)
    package.upload()


gobble.add_command(version)
gobble.add_command(check)
gobble.add_command(pull)
gobble.add_command(push)
gobble.add_command(start)
