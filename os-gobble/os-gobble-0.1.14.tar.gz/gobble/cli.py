"""Command line interface for Gobble"""

import io

from json import loads, dumps
from os import getcwd
from click import command, argument, Path, group, option, echo, Option
from os.path import join
from shutil import rmtree

from gobble.user import create_user, User
from gobble.fiscal import FiscalDataPackage
from gobble.config import ROOT_DIR, settings
from gobble.search import search


@group(name='gobble')
def gobble():
    pass


@command(short_help='Print the version and exit')
def version():
    filename = join(ROOT_DIR, 'package.json')
    with io.open(filename) as json:
        package = loads(json.read())
        echo(package['version'])


@command(short_help='Manage the Gobble user')
@option('create', help='Create a new user or refresh token')
@option('delete', help='Delete the user cache')
@option('show', help='Display user information')
def user(create, delete, show):
    """Manage the Gobble user

    To create a new Gobble user, you need to be registered online. Gobble only
    supports a single user. To switch user account, just create a new user but
    make sure that you copy-paste the authorization link inside a private
    browser window when prompted.

    :param create: create a new user or refresh the user token
    :param delete: erase all files inside the user cache
    :param show: display user information
    """
    user_files = [
        'token.json',
        'permissions.json',
        'authentication.json'
    ]

    if create:
        echo('Welcome to Open-Spending %s' % create_user())
    elif delete:
        rmtree(settings.USER_DIR)
        echo('Deleted local user cache for %s' % User())
    elif show in user_files:
        echo(User._uncache(show) or 'There is no %s cached' % show)


@command(short_help='Validate a datapackage descriptor')
@argument('filepath', type=Path(exists=True), metavar='path to datapackage')
def check(filepath):
    package = FiscalDataPackage(filepath)
    package.validate(raise_error=False)


@command(short_help='Download a fiscal package from Open-Spending')
def pull(package_id, data=False, destination=getcwd()):
    """Download a fiscal package from Open-Spending.

    If no destination folder is provided, the fiscal data package will be
    downloaded to the current working directory. By default, only the package
    `json` descriptor is downloaded, not the data. To include data too, set
    the `data` flag to `True`.

    :param package_id: the unique identifier of the fiscal package
    :param data: whether to download the data files with the descriptor
    :param destination:
    """
    if data:
        raise NotImplemented('Gobble does not yet support data downlaods')

    query = {'title': package_id}
    descriptor = search(query, private=True, limit=1)

    filepath = join(destination, descriptor['title'] + 'json')
    json = dumps(descriptor, ensure_ascii=False, indent=4)
    with io.open(filepath, 'w+', encoding='utf-8') as output:
        output.write(json)

    echo(json)


@command(short_help='Download package descriptors from Open-Spending')
@argument('query_all', required=False)
@option('--private', default=True, help='include private packages')
@option('--limit', default=50, help='limit the search result')
@option('--title', default=None, help='search package title')
@option('--author', default=None, help='search packages by author')
@option('--description', default=None, help='search packages by description')
@option('--region', default=None, help='search packages by region')
@option('--country', default=None, help='search packages by 2-digit country code')
@option('--city', default=None, help='search packages by city')
def search(private,
           limit,
           query_all,
           title,
           author,
           description,
           region,
           country,
           city):
    """Search fiscal packages on Open-Spending.

    You can search a package by `title`, `author`, `description`, `region`,
    `country`, or `city`, or you can match all these fields at once with the magic `q` key.
    Private user packages are included by default if a Gobble user is set up.
    You can limit the size of your results with the `size` parameter.
    """
    search_options = (
        ('title', title),
        ('author', author),
        ('description', description),
        ('regionCode', region),
        ('countryCode', country),
        ('cityCode', city)
    )

    if query_all:
        query = {'q': query_all}
    else:
        query = {key: value for key, value in search_options if value}

    results = search(query, private=private, limit=limit)
    echo(results)


@command(short_help='Upload a datapackage to Open-Spending')
@argument('filepath', type=Path(exists=True))
def push(filepath):
    package = FiscalDataPackage(filepath)
    package.upload()


gobble.add_command(version)
gobble.add_command(check)
gobble.add_command(pull)
gobble.add_command(push)
gobble.add_command(user)
