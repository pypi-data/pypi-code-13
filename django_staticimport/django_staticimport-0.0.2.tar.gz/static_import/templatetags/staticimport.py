from django import template

from static_import.base import (get_static_file as _gf,
                                is_css, is_js, is_img)


register = template.Library()


@register.inclusion_tag('import.html', name='import')
def _import(name, **attr):
    _r = {
        'filename': _gf(name),
        'is_css': is_css(name),
        'is_js': is_js(name),
        'is_img': is_img(name)
    }

    if len(attr) >= 1:
        style = attr.get('style', None)
        if style is not None:
            style = style.replace('"', "'")
            attr['style'] = style

        _r.update(attr)

    return _r
