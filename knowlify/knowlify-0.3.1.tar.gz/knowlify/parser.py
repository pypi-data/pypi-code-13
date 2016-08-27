# Parses HTMLS for juicy hrefs
import requests
import config
from lxml import html


DATA_DIR = config.DATA_DIR


def get_page_from_web(url):
    """
    :type url: str
    :return: HTML file from string
    :type page: html.HtmlElement
    """

    try:
        page = html.document_fromstring(requests.get(url).content)


    except ValueError:
        raise ValueError("Unable to parse URL at %s" % url)

    return page


def append_header(page):
    assert(isinstance(page.head, html.HtmlElement))

    page.head.insert(1, html.Element(
        'script',
        type="text/javascript",
        src='http://aimath.org/knowl.js',

    ))

    page.head.insert(1, html.Element(
        'link',
        href='http://aimath.org/knowlstyle.css',
        rel='stylesheet',
        type='text/css',
    ))

    page.head.insert(1, html.Element(
            'script',
            type='text/javascript',
            src='http://code.jquery.com/jquery-latest.min.js'
    ))

    return page


def swap_href(page):
    #TODO: Create another function that intelligently selects knowlable words/phrases
    for element, attribute, link, pos in page.body.iterlinks():
        if attribute == 'href':
            element.classes._attributes['knowl'] =\
            element.classes._attributes['href']
            element.classes._attributes.pop('href')
    return page

def build_full_page_from_url(url):
    """
    :param url:
    :type url: basestring
    :return: simply knowlified page
    """
    page = get_page_from_web(url)
    page.make_links_absolute(url)
    page = swap_href(page)
    page = append_header(page)
    return page

def build_dummy_page_from_url(url):
    page = get_page_from_web(url)
    return




if __name__ == "__main__":
    pass
