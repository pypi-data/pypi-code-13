from collections import defaultdict

from bs4 import BeautifulSoup
from django.utils import six
from django.utils.safestring import mark_safe, SafeText
from django.utils.text import slugify
from djangocms_text_ckeditor.models import Text

from .conf import settings


def add_ids_to_content(instance, placeholder, rendered_content,
                       original_context):
    # Only patch Text plugins output
    if not isinstance(instance, Text):
        return rendered_content

    text = add_ids(rendered_content, settings.NAV_ELEMENTS, instance.id)

    # Depending on whether the original rendered_content was marked as safe,
    # return a safe string
    if isinstance(rendered_content, SafeText):
        return mark_safe(text)
    else:
        return text


def add_ids(text, tags, prefix=''):
    """
    Add an HTML id attribute to the given list of tags. `text` is the input
    HTML that will be parsed to search for `tags`. The content of the id
    attribute is a slugified version of the tag content. Also a `prefix` can be
    added to the generated ids to avoid collisions (since ids are supposed to
    be unique). This can be used to pass the id of the current placeholder to
    make sure generated ids are unique between placeholders.

    No id will be added on elements that already have an id.

    >>> add_ids('<h2>Hello</h2><p>Paragraph</p><h2>World</h2>', ['h2'])
    '<h2 id="hello">Hello</h2><p>Paragraph</p><h2 id="world">World</h2>'

    >>> add_ids('<h2>Hello</h2><p>Paragraph</p><h2>World</h2>', ['h2'], '99')
    '<h2 id="hello-99">Hello</h2><p>Paragraph</p><h2 id="world-99">World</h2>'

    >>> add_ids('<h2>Hello</h2><p>Hello</p>', ['h2', 'p'])
    '<h2 id="hello">Hello</h2><p id="hello-1">Hello</p>'

    >>> add_ids('<h2>Hello</h2><p>Hello</p>', ['h2', 'p'], '99')
    '<h2 id="hello-99">Hello</h2><p id="hello-99-1">Hello</p>'
    """
    soup = BeautifulSoup(text, settings.XML_PARSER)
    headings = soup.find_all(tags)
    existing_slugs = defaultdict(int)

    for heading in headings:
        slug = slugify(heading.string)

        # Only set the id if there's not already an id
        if 'id' not in heading.attrs:
            heading['id'] = '{slug}{prefix}{suffix}'.format(
                slug=slug,
                prefix='-{}'.format(prefix) if prefix else '',
                suffix='-{}'.format(existing_slugs[slug]) if slug in existing_slugs else ''
            )

        existing_slugs[slug] += 1

    if soup.body:
        return ''.join(six.text_type(t) for t in soup.body)
    else:
        return text
