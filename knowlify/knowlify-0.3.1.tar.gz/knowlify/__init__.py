import worker
import parser
import config
import os
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions



def get_page(file_or_url):
    """

    :param file_or_url: str
    :type url: str
    :return:
    """
    if not os.path.isfile(file_or_url):
        return parser.build_page_from_url(file_or_url)

    else:
        with open(file_or_url, 'r') as f:
            return worker.html.parse(f, base_url=file_or_url)


def output_page(page, path=None):
    if path is None:
        path = page.base_url

    return worker.output_page(page, path)

__all__ = [
    worker,
    parser,
    config,
    get_page,
    output_page,
]
