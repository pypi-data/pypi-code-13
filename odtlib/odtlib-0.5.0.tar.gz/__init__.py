# -*- coding: utf-8 -*-
"""misc utilities catering to openoffice.org xml files manipulations

:organization: Logilab
:copyright: 2008-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import with_statement
from contextlib import contextmanager
from lxml import etree


# Metadata extraction
META_MAP = {'dc:title'             : 'tite',
            'dc:description'       : 'description',
            'dc:date'              : 'date',
            'meta:initial-creator' : 'creator',
            'dc:subject'           : 'subject'}
#           'meta:keyword' :         'keyword'

#59129: Mention Licence GFDL
LICENSE = u'Document diffusé sous licence GNU FDL (http://www.gnu.org/copyleft/fdl.html)'


def read_from_metaxml(xmlstring, attributes):
    """gets a dict of metadata from an xml stream,
    typically from odt/meta.xml
    """
    out = {}
    meta = etree.fromstring(xmlstring)
    for datum in attributes:
        ns, key = datum.split(':')
        elt = meta.find('.//{%s}%s' % (meta.nsmap[ns], key))
        value = elt.text if elt is not None else None
        if isinstance(value, str):
            value = value.decode('utf-8')
        out[datum] = value or u''
    return out

# XXX still used ?
def cut_text(text, cutoff=80):
    if len(text) > cutoff:
        return u'%s[...]' % text[0:cutoff]
    return text

def make_elt(tag, ns, nsmap, text=u'', tail=u'', attrib=dict):
    if attrib is dict: attrib = {}
    elt = etree.Element('{%s}%s' % (nsmap[ns], tag),
                        nsmap=nsmap, attrib=attrib)
    if text:
        elt.text = text
    if tail:
        elt.tail = tail
    return elt

def make_text(tag, nsmap, text=u'', tail=u'', attrib=dict):
    return make_elt(tag, 'text', nsmap, text, tail, attrib)

@contextmanager
def text_ctx(parent, tag, text=u'', tail=u'', attrib=dict):
    elt = make_text(tag, parent.nsmap, text, tail, attrib)
    parent.append(elt)
    yield elt

@contextmanager
def table_ctx(parent, tag, text=u'', tail=u'', attrib=dict):
    """tag in table, table-column, table-row, table-cell
    """
    elt = make_elt(tag, 'table', parent.nsmap, text, tail, attrib)
    parent.append(elt)
    yield elt


def make_style(styles, name, kind='styles', family='paragraph', properties=dict):
    """
    for simple, easy styles
    name='super_title'
    kind='automatic-styles'
    properties={'{%(fo)s}font-size' % nsmap : '24pt',
                '{%(fo)s}font-weight' % nsmap : 'bold',
                '{%(fo)s}font-style' % nsmap : 'italic'}
    """
    nsmap = styles.nsmap
    oostyles = styles.find('.//{%s}%s' % (nsmap['office'], kind))
    the_style = make_elt('style', 'style', nsmap,
                         attrib={'{%(style)s}name' % nsmap : name,
                                 '{%(style)s}family' % nsmap : family})
    style_ppties = make_elt('%s-properties' % family, 'style', nsmap,
                            attrib=properties)
    the_style.append(style_ppties)
    oostyles.append(the_style)
