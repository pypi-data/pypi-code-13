import re
import pytest

from random import choice


PYTEST_PARAM_CHOICES = ['all', 'first', 'last', 'random']
PYTEST_PARAM_DEFAULT = 'all'


def pytest_addoption(parser):
    parser.addoption(
        '--param',
        metavar='choice',
        choices=PYTEST_PARAM_CHOICES,
        default=PYTEST_PARAM_DEFAULT,
        help='test all, first, last or random params (default is %(default)s)')


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    param = config.getoption('param')
    if param != 'all':
        item_chain = {}
        for index, item in enumerate(items):
            # Function.originalname not available in all pytest versions.
            originalname = re.match(r'([^[]+)', item.name).group(0)
            item_chain.setdefault(originalname, [])
            item_chain[originalname].append(item)

        if param == 'first':
            items[:] = [chain[0] for chain in item_chain.values()]
        elif param == 'last':
            items[:] = [chain[-1] for chain in item_chain.values()]
        elif param == 'random':
            items[:] = [choice(chain) for chain in item_chain.values()]
        else:
            raise TypeError('Unsupported param: %s' % param)
