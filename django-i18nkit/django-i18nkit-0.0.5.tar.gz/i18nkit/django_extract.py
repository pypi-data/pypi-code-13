import re

from babel.messages.extract import extract_python
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.six import BytesIO
from django.utils.translation import templatize


def django_extract(fileobj, keywords, comment_tags, options):
    src = force_text(fileobj.read(), settings.FILE_CHARSET)
    src = templatize(src, '')
    if 'gettext(' in src:
        src = re.sub(r'\n\s+', '\n', src)  # Remove indentation
        return extract_python(BytesIO(src.encode('utf8')), keywords, comment_tags, options)
    return ()
