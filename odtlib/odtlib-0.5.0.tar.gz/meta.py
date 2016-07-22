# -*- coding: utf-8 -*-
"""openoffice.org xml files updaters

:organization: Logilab
:copyright: 2008-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import with_statement

from mx.DateTime import now
from lxml import etree
from tempfile import NamedTemporaryFile

from ovcs.package import ODFPackage
from odtlib import (make_elt, make_style, text_ctx, table_ctx, make_text,
                    META_MAP, LICENSE)
from odtlib.utils import tempdir


def create_missing_meta(metanode, ns, tag):
    elt = make_elt(tag, ns, metanode.nsmap)
    metanode.append(elt)
    return elt

def update_styles_definitions(styles):
    ns = styles.nsmap
    make_style(styles, 'FieldDesc', family='text', kind='styles',
               properties={'{%(fo)s}font-size' % ns : '9pt',
                           '{%(style)s}font-size-complex' % ns : '9pt',
                           '{%(fo)s}font-style' % ns : 'italic',
                           '{%(fo)s}font-style-complex' % ns : 'italic',
                           '{%(fo)s}font-weight' % ns : 'normal',
                           '{%(style)s}font-weight-complex' % ns : 'normal'}) # yes, {style} !
    make_style(styles, 'FieldValue', family='text', kind='styles',
               properties={'{%(fo)s}font-size' % ns : '10pt',
                           '{%(fo)s}font-style' % ns : 'italic',
                           '{%(fo)s}font-style-complex' % ns : 'italic',
                           '{%(style)s}font-size-complex' % ns : '10pt',
                           '{%(fo)s}font-weight' % ns : 'normal',
                           '{%(style)s}font-weight-complex' % ns : 'normal'})

    make_style(styles, 'CadreEntete', family='table', kind='automatic-styles',
               properties={'{%(style)s}width' % ns:'17.5cm',
                           '{%(table)s}align' % ns:'margins',
                           '{%(style)s}shadow' % ns:'none',
                           '{%(fo)s}keep-with-next' % ns:'always',
                           '{%(style)s}writing-mode' % ns:'lr-tb'})

    make_style(styles, 'CadreEnteteA', family='table-column', kind='automatic-styles',
               properties={'{%(style)s}column-width' % ns:'11.9cm',
                           #'{%(style)s}rel-column-width' % ns:'6537*'
                           })
    make_style(styles, 'CadreEnteteB', family='table-column', kind='automatic-styles',
               properties={'{%(style)s}column-width' % ns:'2.9cm',
                           #'{%(style)s}rel-column-width' % ns:'1788*'
                           })
    make_style(styles, 'CadreEnteteC', family='table-column', kind='automatic-styles',
               properties={'{%(style)s}column-width' % ns:'2.7cm',
                           #'{%(style)s}rel-column-width' % ns:'1570*'
                           })

    make_style(styles, 'CadreEntete.Cell', family='table-cell', kind='automatic-styles',
               properties={'{%(fo)s}background-color' % ns:'transparent',
                           '{%(style)s}border-line-width-bottom' % ns:'0.002cm 0.035cm 0.002cm',
                           '{%(fo)s}padding' % ns:'0cm',
                           '{%(fo)s}border-left' % ns:'none',
                           '{%(fo)s}border-top' % ns:'none',
                           '{%(style)s}border-bottom' % ns:'0.039cm double #000000'})

    # now, let's hand-cut this thing :
    oostyles = styles.find('.//{%(office)s}styles' % ns)
    # Logo
    logo_style = make_elt('style', 'style', ns,
                          attrib={'{%(style)s}name' % ns : 'LogoCodeAster',
                                  '{%(style)s}display-name' % ns : 'LogoCodeAster',
                                  '{%(style)s}parent-style-name' % ns : 'Header',
                                  '{%(style)s}family' % ns : 'paragraph',
                                  '{%(style)s}class' % ns : 'text'})
    text_ppties = make_elt('text-properties', 'style', ns,
                           attrib={'{%(style)s}font-name' % ns:'Arial',
                                   '{%(fo)s}font-size' % ns : '24pt'})
    para_ppties = make_elt('paragraph-properties', 'style', ns,
                           attrib={'{%(fo)s}padding' % ns:'0cm',
                                   '{%(fo)s}border' % ns:'none',
                                   '{%(style)s}shadow' % ns:'none'})

    logo_style.append(para_ppties)
    logo_style.append(text_ppties)
    # Version
    version_style = make_elt('style', 'style', ns,
                             attrib={'{%(style)s}name' % ns : 'VersionCodeAster',
                                     '{%(style)s}display-name' % ns : 'VersionCodeAster',
                                     '{%(style)s}parent-style-name' % ns : 'Header',
                                     '{%(style)s}family' % ns : 'paragraph',
                                     '{%(style)s}class' % ns : 'text'})
    para_ppties = make_elt('paragraph-properties', 'style', ns,
                           attrib={'{%(fo)s}padding' % ns:'0cm',
                                   '{%(fo)s}border' % ns:'none',
                                   '{%(fo)s}text-align' % ns:'end',
                                   '{%(style)s}shadow' % ns:'none'})
    text_ppties = make_elt('text-properties', 'style', ns,
                           attrib={'{%(style)s}font-name' % ns:'Arial',
                                   '{%(fo)s}font-size' % ns : '12pt'})

    version_style.append(para_ppties)
    version_style.append(text_ppties)
    oostyles.append(logo_style)
    oostyles.append(version_style)

def update_footer(styles, metas):
    """
    example :
    <style:footer>
    <text:p text:style-name="Footer">Manuel de R&#233;f&#233;rence<text:tab/><text:tab/>Fascicule R3.01&#160;: R&#233;f&#233;rences g&#233;n&#233;rales</text:p>
    </style:footer>
    """
    master_styles = styles.find('.//{%s}master-styles' % styles.nsmap['office'])
    footer = master_styles.find('.//{%s}footer' % master_styles.nsmap['style'])
    if footer is None:
        footer = create_missing_meta(master_styles, 'style', 'footer')
    footer.clear()
    with text_ctx(footer, 'p', text=metas['doctype_title'],
                  attrib={'style-name':'Footer'}) as para:
        para.append(make_text('tab', para.nsmap))
        para.append(make_text('tab', para.nsmap, tail=u'Fascicule %s : %s' %
                    (metas['category'], metas['cat_title'])))
    # XXX make a interstice (could be better styled by paragraph rules)
    footer.append(make_text('p', footer.nsmap, text=u'   ', attrib={'style-name':'Footer'}))
    with text_ctx(footer, 'p', attrib={'style-name':'Footer'}) as para:
        para.append(make_text('span', para.nsmap, text=LICENSE))


def update_header(styles, metas):
    """wholesale replacement of the header section
    note that some documents exhibit several such sections ...
    some additional claning might be needed
    """
    master_styles = styles.find('.//{%(office)s}master-styles' % styles.nsmap)
    # header
    header = master_styles.find('.//{%(style)s}header' % master_styles.nsmap)
    if header is None:
        header = create_missing_meta(master_styles, 'style', 'header')
    header.clear()
    ns = header.nsmap
    text_style = '{%(text)s}style-name' % ns
    table_style = '{%(table)s}style-name' % ns
    with table_ctx(header, 'table', attrib={'{%(table)s}name' % ns : 'CadreEntete',
                                            table_style : 'CadreEntete'}) as table:
        wt = table.append
        for col in 'ABC':
            wt(make_elt('table-column', 'table', ns,
                       attrib={table_style:'CadreEntete%s' % col}))

        with table_ctx(table, 'table-row') as row:
            with table_ctx(row, 'table-cell', attrib={table_style:'CadreEntete.Cell',
                                                      '{%(office)s}value-type' % ns:'string'}) as cell:
                cell.append(make_text('p', ns, text=metas['project_name'],
                                      attrib={text_style:'LogoCodeAster'}))
            with table_ctx(row, 'table-cell', attrib={table_style:'CadreEntete.Cell',
                                                      '{%(office)s}value-type' % ns:'string'}) as cell:
                cell.append(make_text('p', ns))
            with table_ctx(row, 'table-cell', attrib={table_style:'CadreEntete.Cell',
                                                      '{%(office)s}value-type' % ns:'string'}) as cell:
                cell.append(make_text('p', ns, text=u'Version %s' % metas['ca_version'],
                                      attrib={text_style:'VersionCodeAster'}))

        with table_ctx(table, 'table-row') as row:
            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-texte'}) as p:
                    p.append(make_text('span', ns, text=u'Titre : ',
                                       attrib={text_style:'FieldDesc'}))
                    p.append(make_text('span', ns, text=metas['title'],
                                       attrib={text_style:'FieldValue'}))

            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-texte'}) as p:
                    p.append(make_text('span', ns, text=u'Date : ',
                                       attrib={text_style:'FieldDesc'}))
                    date = metas['date'] or now()
                    p.append(make_text('span', ns, text=unicode(date.strftime('%d/%m/%Y')).split()[0],
                                       attrib={text_style:'FieldValue'}))

            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-texte'}) as p:
                    p.append(make_text('span', ns, text=u'Page : ', attrib={text_style:'FieldDesc'}))

                    with text_ctx(p, 'span', attrib={text_style:'FieldValue'}) as currpage:
                        currpage.append(make_text('page-number', ns, text=u'42',
                                                  attrib={'{%(text)s}select-page' % ns: u'current'}))

                    p.append(make_text('span', ns, text=u'/', attrib={text_style: 'FieldValue'}))

                    with text_ctx(p, 'span', attrib={text_style: 'FieldValue'}) as page_count:
                        page_count.append(make_text('page-count', ns, text=u'42',
                                                    attrib={'{%(style)s}numformat' % ns : '1'}))

        with table_ctx(table, 'table-row') as row:
            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-text'}) as p:
                    p.append(make_text('span', ns, text=u'Responsable : ',
                                       attrib={text_style:'FieldDesc'}))
                    p.append(make_text('span', ns, text=metas['initial_creator'],
                                       attrib={text_style:'FieldValue'}))
            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-texte'}) as p:
                    p.append(make_text('span', ns, text=u'Clé : ',
                                       attrib={text_style:'FieldDesc'}))
                    p.append(make_text('span', ns, text=metas['keyword'].upper(),
                                       attrib={text_style:'FieldValue'}))
            with table_ctx(row, 'table-cell', attrib={'{%(office)s}value-type' % ns:'string'}) as cell:
                with text_ctx(cell, 'p', attrib={text_style:u'Entête-texte'}) as p:
                    p.append(make_text('span', ns, text=u'Révision : ',
                                       attrib={text_style:'FieldDesc'}))
                    p.append(make_text('span', ns, text=metas.get('revision', 'n/a'),
                                       attrib={text_style:'FieldValue'}))
        header.append(make_text('p', ns, text=u'   ', attrib={text_style:u'Entête-texte'}))

def stream_with_injected_metadata(odtstream, metas):
    """return odt stream with updated metadata"""
    with tempdir() as tempd:
        sodt = ODFPackage.fromstream(odtstream)
        odt = sodt.unzipped(tempd, overwrite=True, mode='w')
        # inject matadata
        meta_xml = odt.data('meta.xml')
        meta = etree.fromstring(meta_xml)
        for datum in META_MAP.keys():
            ns, key = datum.split(':')
            elt = meta.find('.//{%s}%s' % (meta.nsmap[ns], key))
            if elt is None:
                elt = create_missing_meta(meta, ns, key)
            elt.text = unicode(metas[key.replace('-', '_')])
        odt.write('meta.xml', etree.tostring(meta, pretty_print=True))
        # set it also in styles.xml (controls header/footer for each page)
        styles_xml = odt.data('styles.xml')
        styles = etree.fromstring(styles_xml)
        update_styles_definitions(styles)
        update_header(styles, metas)
        update_footer(styles, metas)
        odt.write('styles.xml', etree.tostring(styles, pretty_print=True))
        # file('/home/auc/styles.xml', 'w').write(etree.tostring(styles, pretty_print=True))
        with NamedTemporaryFile() as tmp:
            return open(odt.zipped(tmp.name, overwrite=True).path).read()
