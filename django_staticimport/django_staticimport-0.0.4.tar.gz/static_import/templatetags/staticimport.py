from django import template

from static_import.base import (get_static_file as _gf,
                                is_css, is_js, is_img,
                                is_remote, is_local, 
                                safe_extra_attrs)


register = template.Library()


@register.inclusion_tag('import.html', name='import')
def _import(name, **attr):
    fn, wt = _gf(name)

    rs = {
        'filename': fn,
        'is_css': is_css(fn),
        'is_js': is_js(fn),
        'is_img': is_img(fn),
        'is_local': is_local(wt),
        'is_remote': is_remote(wt)
    }

    if len(attr) >= 1:
        rs.update(safe_extra_attrs(attr))

    return rs
