# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Experimental Segno converter plugin to create SVG (Micro) QR Codes with some
effects.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import xml.etree.ElementTree as etree
import io
import copy
import random
import re
try:  # pragma: no-cover
    range = xrange  # Python 2
except NameError:  # pragma: no-cover
    pass
from segno import encoder, colors

__version__ = '0.1.1'

_SVG_NS = 'http://www.w3.org/2000/svg'
_XLINK_NS = 'http://www.w3.org/1999/xlink'

# Used to minimize the XML
_REMOVE_WS_PATTERN = re.compile(r'(>)\s+(<)')


def _make_defs_if_not_exists(svg):
    """\
    Adds a <defs/> element to the SVG iff it not exists.

    :param svg: etree.Element
    """
    el_defs = svg.find('{{{0}}}defs[1]'.format(_SVG_NS))
    if el_defs is None:
        el_defs = _make_svg_element('defs')
        svg.insert(0, el_defs)
    return el_defs


def _find_last_path(svg):
    """\
    Returns the last within the SVG document.

    :param svg: etree.Element
    """
    return svg.find('{{{0}}}path[last()]'.format(_SVG_NS))


def _parse_element(xml):
    """\
    Parses the provided XML and returns an etree.Element.

    :param str xml: The string to parse.
    """
    return etree.fromstring(_REMOVE_WS_PATTERN.sub(r'\1\2', xml))


def _make_svg_element(name, **kw):
    """\
    Factory function to create an element in the SVG namespace.
    """
    return etree.Element('{{{0}}}{1}'.format(_SVG_NS, name), **kw)


def _make_use_el(href, **kw):
    """\
    Creates <use href=..."/> element.
    """
    kw['{{{0}}}href'.format(_XLINK_NS)] = href
    return _make_svg_element('use', **kw)


def _write_xml(xml, out, **kw):
    """\
    Serializes the provided etree.

    :param xml.etree.ElementTree: The etree to serialize
    :param out: Output stream
    :param \**kw: Any keywords, but only 'encoding' and 'xmldecl' is evaluated.
    """
    xml.write(out, encoding=str(kw.get('encoding', 'utf-8')),
              xml_declaration=kw.get('xmldecl', True))


def _write_filter(qrcode, out, filter, filter_id, postparse_callback=None, **kw):
    """\

    :param filter: etree.Element or str
    :param filter_id: The filter identifier.
    :param qrcode: The :py:class:`segno.QRCode`.
    """
    xml = as_etree(qrcode, **kw)
    svg = xml.getroot()
    path = _find_last_path(svg)
    if postparse_callback is not None:
        postparse_callback(svg, path)
    el = filter if isinstance(filter, etree.Element) else _parse_element(filter)
    el.attrib['id'] = filter_id
    _make_defs_if_not_exists(svg).append(el)
    path.attrib['filter'] = 'url(#{0})'.format(filter_id)
    _write_xml(xml, out, **kw)


def write_glow(qrcode, out, filter_id='segno-glow', deviation=.6, **kw):
    """\
    Creates a "glow" effect.

    :param qrcode: The :py:class:`segno.QRCode`.
    :param out: Filename or a file-like object supporting to write bytes.
    :param str filter_id: Name of the filter.
    :param float deviation: Indicates the standard deviation for the blur
            operation, default: ``.6``.
    :param \**kw: SVG parameters, see segno.QRCode.svg
    """
    s = '''<filter filterUnits="userSpaceOnUse">
<feGaussianBlur stdDeviation="{0}" in="SourceGraphic" result="coloredBlur"/>
  <feMerge>
    <feMergeNode in="coloredBlur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>'''.format(deviation)
    _write_filter(qrcode, out, s, filter_id=filter_id, **kw)


def write_blur(qrcode, out, filter_id='segno-blur', deviation=.3, **kw):
    """\

    :param qrcode: The :py:class:`segno.QRCode`.
    :param out: Filename or a file-like object supporting to write bytes.
    :param str filter_id: Name of the filter.
    :param \**kw: SVG parameters, see segno.QRCode.svg
    """
    s = '''<filter>
       <feGaussianBlur in="SourceGraphic" stdDeviation="{0}" />
    </filter>'''.format(deviation)
    _write_filter(qrcode, out, s, filter_id=filter_id, **kw)


def write_pacman(qrcode, out, pacman_color='#fc0', dot_color='#fc0', ghosts=5,
                 ghost_colors=('#ff0c13', '#f2aeaf', '#1bb1e6', '#f97e16'),
                 **kw):
    """\

    :param qrcode: The :py:class:`segno.QRCode`.
    :param out: Filename or a file-like object supporting to write bytes.
    :param pacman_color:
    :param dot_color:
    :param ghosts:
    :param ghost_colors:
    :param \**kw: SVG parameters, see segno.QRCode.svg
    """
    smiley_el = _parse_element('<path d="M.947.724a.5.5 0 1 1 .001-.446l-.448.222z" transform="scale(.8)"/>')
    smiley_el.attrib['fill'] = colors.color_to_webcolor(pacman_color)
    xml = as_etree(qrcode, **kw)
    svg = xml.getroot()
    defs_el = _make_defs_if_not_exists(svg)
    dot_el = _parse_element('<circle id="dot" cx="1" cy="1" r=".5" stroke="none" transform="scale(.2)"/>')
    dot_el.attrib['fill'] = colors.color_to_webcolor(dot_color)
    defs_el.append(dot_el)
    if ghosts > 0:
        defs_el.append(etree.Comment('''
The "ghost" was created by James Fenton
Source:  <https://thenounproject.com/term/pacman/193957/>
License: CC BY 3.0 US - <https://creativecommons.org/licenses/by/3.0/us/>
'''))
        ghost_el = _parse_element('<g id="ghost" transform="scale(.08)"><circle cx="6.588" cy="4.515" r=".526"/><path d="M4.031 0c-2.136 0-3.883 1.663-4.02 3.757h-.011v5.799s.232.663.926-.168c.705-.831 1.21.168 1.21.168s.547 1 1.21 0c.663-1 1.315 0 1.315 0s.61.852 1.168 0c.558-.852 1.116-.168 1.116-.168s1.073 1.158 1.073 0c0-.863.042-5.157.042-5.357 0-2.221-1.8-4.031-4.031-4.031zm-.295 5.736c-.579 0-1.052-.547-1.052-1.231 0-.674.474-1.231 1.052-1.231.579 0 1.052.547 1.052 1.231s-.463 1.231-1.052 1.231zm2.515 0c-.579 0-1.052-.547-1.052-1.231 0-.674.474-1.231 1.052-1.231.579 0 1.052.547 1.052 1.231s-.474 1.231-1.052 1.231z"/><circle cx="4.073" cy="4.515" r=".526"/></g>')
        defs_el.append(ghost_el)
    version = encoder.normalize_version(qrcode.version)
    function_matrix = encoder.make_matrix(version, reserve_regions=False, add_timing=False)
    encoder.add_finder_patterns(function_matrix, version < 1)
    encoder.add_alignment_patterns(function_matrix, version)

    def is_data_area(y, x):
        return function_matrix[y][x] == 0x2

    matrix = qrcode.matrix
    max_length = -1
    row_idx = -1
    col_idx = -1
    for i in range(len(matrix)):
        length = 0
        for j in range(len(matrix)):
            if is_data_area(i, j) and matrix[i][j]:
                length += 1
                if length > max_length:
                    max_length = length
                    row_idx = i
                    col_idx = j - max_length + 1
            else:
                length = 0
    border = kw.get('border', qrcode.default_border_size)
    scale = kw.get('scale', 1)
    g_el = _make_svg_element('g')
    path = _find_last_path(svg)
    svg.remove(path)
    svg.append(g_el)
    g_el.append(path)
    if scale > 1:
        g_el.attrib['transform'] = 'scale({0})'.format(scale)
        del path.attrib['transform']
    smiley_g = _make_svg_element('g')
    offset = 0
    if max_length > 2:
        offset = 1
    smiley_g.attrib['transform'] = 'translate({0}, {1})'.format(col_idx + offset + border + .1,
                                                                row_idx + border + .1)
    smiley_g.append(smiley_el)
    smiley_g.extend([_make_use_el('#dot', x=str(i + 1.2), y='.2') for i in range(max_length - 2)])
    g_el.append(smiley_g)
    if ghosts > 0:
        ghost_groups = [_make_svg_element('g', fill=colors.color_to_webcolor(clr)) for clr in ghost_colors]
        ghost_count = 0
        ghost_matrix = copy.deepcopy(matrix)
        ghost_matrix[row_idx][col_idx:col_idx + max_length] = b'\0' * max_length
        size = len(matrix) - 1
        while ghost_count < ghosts:
            x, y = random.randint(0, size), random.randint(0, size)
            if is_data_area(y, x) and ghost_matrix[y][x] == 0x1:
                ghost_matrix[y][x] = 0x0
                if ghost_matrix[max(0, y - 1)][x] == 0x0 \
                        and ghost_matrix[min(size, y + 1)][x] == 0x0 \
                        and ghost_matrix[y][min(size, x + 1)] == 0x0 \
                        and ghost_matrix[y][max(0, x - 1)] == 0x0:
                    continue
                ghost_count += 1
                random.choice(ghost_groups).append(_make_use_el('#ghost',
                                                    x=str(x + border + .2),
                                                    y=str(y + border + .1)))
        g_el.extend([ghost_group for ghost_group in ghost_groups if len(ghost_group)])
    _write_xml(xml, out, **kw)


def as_etree(qrcode, **kw):
    """\
    Returns the provided `qrcode` as SVG ElementTree.

    :param qrcode: The :py:class:`segno.QRCode`.
    :param \**kw: SVG parameters, see py:method:`segno.QRCode.save()`
    :rtype: :py:class:`xml.etree.ElementTree`
    """
    buff = io.BytesIO()
    qrcode.save(buff, kind='svg', **kw)
    buff.seek(0)
    return etree.parse(buff)


etree.register_namespace('', _SVG_NS)
etree.register_namespace('xlink', _XLINK_NS)
