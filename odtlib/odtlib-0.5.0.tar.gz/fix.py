# -*- coding: utf-8 -*-
"""openoffice.org xml files updaters

:organization: Logilab
:copyright: 2008, 2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import with_statement
from tempfile import NamedTemporaryFile

from lxml import etree

from ovcs.package import StreamODFPackage

from odtlib import make_text, make_style
from odtlib.utils import tempdir

# legend types ((type, num-format)) for Table, Figure, Illustration and equation sequences
LEGEND_TYPES = {u'Table':  {'num_fmt' : '1'},
                u'éq':    {'num_fmt' : '1'},
                u'Figure': {'num_fmt' : 'a' },
                # 'Drawing':{'num_fmt': 'a' },
                # 'Illustration': {'num_fmt':'a'}
                }
# authorized list styles
LIST_STYLES =  (u'ListeN', u'ListeP', u'Biblio')


def node_uses_font(tree, node, fonts):
    styleref = '{%(text)s}style-name' % node.nsmap
    nodeattrs = dict(node.items())
    stylename = nodeattrs.get(styleref, None)
    if stylename is None:
        return False
    if stylename:
        try:
            style = lookup_style_by_name(tree, stylename)[0]
        except:
            # XXX style_name like "Standard"
            #     need to loopup into styles.xml ?
            print 'WARNING: do not know the font of', repr(stylename)
            return False
        return font_of_style(style) in fonts
    return False

def font_of_style(node):
    fontref = '{%(style)s}font-name' % node.nsmap
    for child in node.iterchildren():
        chattrs = dict(child.items())
        if fontref in chattrs:
            return chattrs[fontref]

def replace_chunk(tree, node, attr, charmap, font, newstyle_name):
    ns = tree.nsmap
    chunk = getattr(node, attr, None)
    if chunk is not None:
        for val in charmap:
            if val in chunk:
                new_style = lookup_style_by_name(tree, newstyle_name)
                if len(new_style) == 0:
                    make_style(tree, newstyle_name,
                               family='text', kind='automatic-styles',
                               properties={'{%(style)s}font-name' % ns  : font})
                styleref = '{%(text)s}style-name' % ns
                span = make_text('span', ns, text=charmap[val],
                                 tail = chunk[chunk.index(val)+1:],
                                 attrib={styleref : newstyle_name})
                setattr(node, attr, chunk[:chunk.index(val)])
                if attr == 'text':
                    node.append(span)
                else:
                    node.getparent().append(span)
                replace_chunk(tree, span, 'tail', charmap, font, newstyle_name)

def replace_text_nodes_and_font_using(tree, charmap, fontmap):
    """replace all occurrences of charmap keys by
    the values, also collecting the style of places where replacement
    happened
    we well put replacements in spans using a new automatic text-family style
    """
    used_font, font_to_use = fontmap.items()[0]
    new_style_name = 'T%s' % font_to_use.upper().replace(' ', '')
    for node in tree.getiterator():
        if not node_uses_font(tree, node, [used_font]):
            continue
        for attr in ('text', 'tail'):
            replace_chunk(tree, node, attr, charmap, font_to_use, new_style_name)

def replace_text_nodes_using_font(tree, charmap, font):
    """replace all occurrences of charmap keys by the values
    in nodes using style using font
    """
    for node in tree.getiterator():
        if node_uses_font(tree, node, [font]):
            for attr in ('text', 'tail'):
                chunk = getattr(node, attr, None)
                match = False
                if chunk is not None:
                    for val in charmap:
                        if val in chunk:
                            match = True
                            chunk = chunk.replace(val, charmap[val])
                    if match:
                        setattr(node, attr, chunk)

def lookup_style_by_name(tree, stylename):
    """find and return all nodes defining stylename
    (afaik there should be, on average, one :)"""
    allnodes = tree.findall('.//{%(style)s}style' % tree.nsmap)
    nodes = []
    for node in allnodes:
        nameattr = '{%(style)s}name' % node.nsmap
        name = node.get(nameattr)
        if name in stylename:
            nodes.append(node)
    return nodes


def update_text_and_fonts(tree, text_replacement_map, fontmap):
    """replace all text occurrences and change the font of
    the automatic styles according to the fontmap
    """
    replace_text_nodes_and_font_using(tree, text_replacement_map, fontmap)

def update_toc(content):
    """
    replace the header "Table of contents" style by Tdm (if any)
    <text:index-title-template text:style-name="Contents_20_Heading">Table des matières</text:index-title-template>
       and
    <text:index-title text:style-name="Sect2" text:name="Table of ContentsX&_Head">
      <text:p text:style-name="Tdm">Table of Contents</text:p>
    </text:index-title>
    """
    nsmap = content.nsmap
    title_nodes = content.findall('.//{%(text)s}index-title-template' % nsmap)
    for title_node in content.findall('.//{%(text)s}index-title' % nsmap):
        title_nodes.append(title_node.getchildren()[0])
    for title in title_nodes:
        title.set('{%(text)s}style-name' % nsmap, 'Tdm')
        # replace the title by "Table des Matières"
        title.text = u'Table des Matières'

def get_last_sequence_ref(content, label):
    """get the last reference for a sequence type (Table, Illustration, etc)"""
    nsmap = content.nsmap
    tab_expr = ".//{%(text)s}sequence[@{%(text)s}name=" % nsmap +  "'%s']" % label
    refs = []
    for seq in content.findall(tab_expr):
        ref_name = seq.get('{%(text)s}ref-name' % nsmap)
        refs.append(int(ref_name.split("ref"+label)[1]))
    return refs and max(refs) or 0

def add_table_sequence(content, node, label, num_format, text_label):
    """
    Generate and add a new sequence for a type "label" (Table, Illustration, etc)
    text : translation of label
    num_format : check self.legend_types
    """
    nsmap = content.nsmap
    ref = get_last_sequence_ref(content, label)
    text = "{%(text)s}" % nsmap
    style = "{%(style)s}" % nsmap
    wrap_attrib = {'%sstyle-name' % text: label}
    wrap =  etree.Element('{%(text)s}p' % nsmap, attrib=wrap_attrib)
    wrap.text = text_label
    seq_attrib = {"%sref-name" % text: "ref%s%d" % (label, ref+1),
              "%sname" % text: "%s" % label,
              "%sformula" % text:"ooow:%s+1" % label,
              "%snum-format" % style: num_format
              }
    sequence = etree.Element('{%(text)s}sequence' % nsmap, attrib=seq_attrib)
    wrap.append(sequence)
    node.addnext(wrap)

def update_table_sequences(content):
    """
    Create missing legends for tables
    """
    nsmap = content.nsmap
    for table_node in  content.findall('.//{%(table)s}table' % nsmap):
        next_node = table_node.getnext()
        if next_node is None:
	    # table in a table
            continue
        if next_node.find(".//{%(text)s}sequence" % nsmap) is None:
	    # we add the missing legend
            add_table_sequence(content, table_node, "Table", "1", u"Tableau ")

def update_list_styles(content, styles_etree, refstyles_etree):
    """
    replace all paragraphes or contained in a list (having
    the style as list-style-name) by ListN and ListP styles except
    the paragraphes with one of authorized styles (LIST_STYLES)

    styles definition :

    · If the list is contained within another list, the list style defaults to the style of the surrounding
    list.

    · If there is no list style specified for the surrounding list, but the list contains paragraphs that
    have paragraph styles attached specifying a list style, this list style is used for any of these
    paragraphs.

    · A default list style is applied to any other paragraphs.
    """
    nsmap = content.nsmap

    def get_list_style(content, nsmap, set_prop=False):
        """return the new style based on old style definition"""
	# XXX why level = 1
	# bullets list
        bullets = content.find(".//{%(text)s}list-level-style-bullet[@{%(text)s}level='1']" % nsmap)
	# numbered list
        num_fmt =  content.find(".//{%(text)s}list-level-style-number[@{%(text)s}level='1']" % nsmap)
        if bullets is not None:
            # set default bullet
            for bullet in content.findall(".//{%(text)s}list-level-style-bullet" % nsmap):
                if set_prop:
                    prop = bullet.find(".//{%(style)s}text-properties" % nsmap)
                    if prop is None:
                        prop = etree.Element('{%(style)s}text-properties' % nsmap,
					     attrib={'{%(style)s}font-name' % nsmap: u"Symbol"})
                        bullet.append(prop)
		    # XXX does not work
		    # prop.set('{%(style)s}font-name' % nsmap, u"Symbol")
                bullet.set('{%(text)s}bullet-char' % nsmap, u"\u2022")
            return  u"ListeP"
        else:
            assert num_fmt is not None
	    # set number formatting as numeric : 1, 2, 3 style:num-format="1"
            for node in num_fmt:
                node.set("{%(style)s}num-format" % nsmap, "1")
            return u"ListeN"

    # try to find on the fly list style definitions and process them
    # list_names = set([ l.get('{%(text)s}style-name' % nsmap) for l in list_styles])
    for list_style_node in content.findall(".//{%(text)s}list" % nsmap):
	# listeN is the default style
        list_style_name =  list_style_node.get('{%(text)s}style-name' % nsmap)
        new_style = u"ListeN"
        # temporary set the new style in self.nsmap
        nsmap.update({'lsn' : list_style_name})
	# look for style's definition in content.xml first
        list_def = content.find(".//{%(text)s}list-style[@{%(style)s}name='%(lsn)s']" % nsmap)
        if list_def is not None:
            new_style = get_list_style(list_def, nsmap, set_prop = True)
        else:
	    # then look for style's definition in styles.xml
            list_def = styles_etree.find(".//{%(text)s}list-style" % styles_etree.nsmap)
            if list_def is not None:
                new_style = get_list_style(list_def, styles_etree.nsmap)

        # search for paragraphes or heading contained in a list
        # (having the style as list-style-name)
        for def_node in content.findall(".//{%(style)s}style[@{%(style)s}list-style-name='%(lsn)s']" % nsmap):
            p_style_name = def_node.get('{%(style)s}parent-style-name' % nsmap)
            family = def_node.get('{%(style)s}family' % nsmap)
            # we only do it for paragraphes
            if family == 'paragraph' and p_style_name not in LIST_STYLES:
                def_node.set('{%(style)s}parent-style-name' % nsmap, new_style)
        # clean nsmap XXX having a updated(dict, dict) -> dict would be saner
        nsmap.pop('lsn', None)

def update_sequences_decl(content):
    """
     update sequences declaration in content.xml:
      - add missing sequences ('éq', 'Figure')
      - update "display-outline-level" and "separation-character" attributes
     <text:sequence-decl text:display-outline-level="4" text:separation-character="-" text:name="Table"/>
    """
    nsmap = content.nsmap
    seqs = []
    sec_decls_node = content.find(".//{%(text)s}sequence-decls" % nsmap)
    for dtype in LEGEND_TYPES.keys():
        seq = content.find(".//{%(text)s}sequence-decl[@{%(text)s}name='%(dtype)s']" % \
                               {'text' : content.nsmap['text'], 'dtype': dtype})
        if seq is not None:
            seqs.append(seq)
        else:
            # add missing sequences ('éq', 'Figure')
            attrib = {'{%(text)s}name' % nsmap : dtype}
            elt = etree.Element('{%(text)s}sequence-decl' % nsmap, attrib=attrib)
            sec_decls_node.append(elt)
            seqs.append(elt)
    for node in seqs:
        node.set("{%(text)s}display-outline-level" % nsmap, "4")
        node.set("{%(text)s}separation-character" % nsmap, "-")

def update_sequences_in_content(content):
    """
    set Caption style on all Table, Figure, Illustration and eq sequences
    set the right num-format : "a" for   Figure and Illustration, "1" for Table and eq
    """
    nsmap = content.nsmap
    sequences = {}
    for dtype, attrs in LEGEND_TYPES.items():
        elmts = content.findall(".//{%(text)s}sequence[@{%(text)s}name='%(dtype)s']" % \
                                    {'text': nsmap['text'], 'dtype': dtype})
        for elt in elmts:
            sequences.update({elt:attrs['num_fmt']})
    for node, num_format in sequences.items() :
        pnode = node.getparent()
        pnode.set("{%(text)s}style-name" % nsmap, "Caption")
        node.set("{%(style)s}num-format" % nsmap, num_format)


def apply_fonts_substitutions(content, fontmap, fontcharmaps):
    """replace all fonts provided in the font substitution mapping"""
    # keep styles without explicit font declaration
    ns = content.nsmap
    # look up for style definitions
    for textprop_node in content.findall(".//{%(style)s}text-properties" % ns):
        fontattr = '{%(style)s}font-name' % ns
        font = textprop_node.attrib.get(fontattr)
        if font:
            textprop_node.set(fontattr, fontmap.get(font, font))
    for fontcharmap in fontcharmaps:
        font, charmap = fontcharmap.items()[0]
        replace_text_nodes_using_font(content, charmap, font)


# TOP-LEVEL
def fixup_styles(odtstream, params, refstyle):
    """return odt stream with styles fixed"""
    refstyle_etree = etree.fromstring(refstyle)
    with tempdir() as tempd:
        params.pop('eid', None)
        odt = StreamODFPackage(odtstream).unzipped(tempd, overwrite=True, mode='w')
        content_etree = etree.fromstring(odt.data('content.xml'))
        content_etree.nsmap.update({'eq': u'éq'})
        styles_etree = etree.fromstring(odt.data('styles.xml'))
        styles_etree.nsmap.update({'eq': u'éq'})
        update_toc(content_etree)
        if params.pop('table_legends', None):
            update_table_sequences(content_etree)
        update_list_styles(content_etree, styles_etree, refstyle_etree)
        # update_table_styles()
        update_sequences_decl(content_etree)
        update_sequences_in_content(content_etree)
        charmaps = params.pop('char_translation_table', None)
        apply_fonts_substitutions(content_etree, params, charmaps)
        trf = params.pop('charfont_translation_table', None)
        if trf:
            for fontmap, charmap in trf:
                update_text_and_fonts(content_etree, charmap, dict([fontmap]))
        odt.write('content.xml', etree.tostring(content_etree, pretty_print=True))
	# replace styles.xml by references styles
        odt.write('styles.xml', refstyle)
        if 'layout-cache' in odt.subelements():
            # will confuse oowriter if present now
            odt.remove('layout-cache')
        with NamedTemporaryFile() as tmp:
            return open(odt.zipped(tmp.name, overwrite=True).path).read()
