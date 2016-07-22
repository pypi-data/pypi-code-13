# -*- coding: utf-8 -*-
"""a lint for odt documents (wrt some reference style sheet)

:organization: Logilab
:copyright: 2008-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import with_statement

import re
from lxml import etree

from cubicweb.gettext import translation

from logilab.common.textutils import unormalize
from logilab.mtconverter import xml_escape
from ovcs.package import StreamODFPackage

from odtlib import cut_text, i18n

EXCLUDED_STYLE = ('graphic',)
ALLOWED_FONTS = (u'Arial', u'Courier New', u'OpenSymbol')

# any font having the key in its .lower() should be
# considered equal to, or ripe for replacement by the value
FONTS_SUBSTITUTIONS = {'courier'  : u'Courier New',
                       'symbol'   : u'OpenSymbol',
                       'arial'    : u'Arial'}

_ = unicode

def canonical_font(fontname):
    """ returns the canonical fontname matching an arbitrary fontname
        (and a bool telling if the match is exact), or None
    ex : 'Courier 10 Pitch' -> 'Courier New', False
         'Arial' -> 'Arial', True
         'Nimbus Roman No9 L' -> None, None
    NOTE : one could get smarter than that and go through
           generic font families mappings
           and make all these mappgins editable through the gui
    """
    name = fontname.lower()
    for font in FONTS_SUBSTITUTIONS:
        if font in name:
            cfont = FONTS_SUBSTITUTIONS[font]
            return FONTS_SUBSTITUTIONS[font], fontname == cfont
    return None, None

def pretty_style_name_from_node(node, nsmap):
    name =node.get('{%(style)s}display-name' % nsmap)
    if name is None:
        name = pretty_style_name(node.get('{%(style)s}name' % nsmap))
    return name

def pretty_style_name(name):
    return name.replace('_20_', ' ')

def process_text_node(text):
    """returns a normalized, xml_escaped unicode string
    """
    if text is None:
        return u''
    text = normalize_whitespaces(text)
    return text if isinstance(text, unicode) else unicode(text, 'utf-8')

def normalize_whitespaces(text):
    return re.sub(r'(\s)+', ' ', text).strip()

def unescaped_text(node):
    try:
        #text = etree.tostring(node, encoding='utf-8', method="text")
        # XXX kill the XXX below ?
        text = ''.join(node.xpath('.//text()'))
    except: # XXX suspect windows apostrophe caracter \u2019 || lxml weirdness
        text = ' '.join([node.text if node.text else u'',
                         node.tail if node.tail else u''])
    return text

def escaped_text(node):
    """
    XXX for some reason not all text is unicode
    we better rewrite our function
    """
    return xml_escape(process_text_node(unescaped_text(node)))

def get_office_version(content):
    return content.get('{%(office)s}version' % content.nsmap )

def get_used_content_styles(content, with_table_styles=True):
    """get styles from"""
    nsmap = content.nsmap
    styles = {}
    for text_node in content.xpath(".//*[starts-with(name(), 'text')]"):
        name = text_node.get('{%(text)s}style-name' % nsmap)
        # XXX we should also retrive the style family
        if name :
            styles.setdefault(name, []).append(text_node)
    if with_table_styles:
        for table_node in content.xpath(".//*[starts-with(name(), 'table')]"):
            name = table_node.get('{%(table)s}style-name' % nsmap)
            if name :
                styles.setdefault(name + ":table", []).append(table_node)
    return styles

def get_unused_styles(content,  show_automatic_styles=False):
    """check all unused styles in content.xml and styles.xml"""
    nsmap = content.nsmap
    styles = [(s.get("{%(style)s}name" % nsmap), s.get("{%(style)s}family" % nsmap)) \
              for s in content.findall(".//{%(style)s}style" % nsmap)]
    # XXX get_used_content_styles sould have styles family
    used_styles = get_used_content_styles(content)
    unused_styles = set([s for s, f in styles]).difference(used_styles.keys())
    if not show_automatic_styles:
        unused_styles = [(s, f) for s, f in styles
                         if s in unused_styles and not automatic_style(s, f)]
    return list(sorted(unused_styles))

def normalize_fontfamily(familyname):
    return familyname.strip().replace("'", "")

def get_font_families(content, styles):
    """retrieve font mapping to their (merged) families
    ex: style:font-face style:name="Geneva" svg:font-family="Geneva, Arial"
    see:
          http://en.wikipedia.org/wiki/Font_family_(HTML)
          http://en.wikipedia.org/wiki/Font_family
    """
    font_families = {}
    content_fonts = content.findall(".//{%(style)s}font-face" % content.nsmap)
    styles_fonts = styles.findall(".//{%(style)s}font-face" % styles.nsmap)
    for font in content_fonts + styles_fonts:
        font_family = font.get('{%(svg)s}font-family' % content.nsmap).split(',')
        name = font.get('{%(style)s}name' % content.nsmap)
        font_families.setdefault(name, []).extend([normalize_fontfamily(f)
                                                   for f in font_family])
    return dict((k, set(v))
                for k, v in font_families.iteritems())

def get_style_properties(node, style_ns):
    """
    node     : style node
    style_ns : nsmap['style']
    """
    attrs = {}
    attr_to_filter = ('asian', 'complex')
    for child in node.iterchildren():
        for attr in child.attrib:
            # we are only interested in "style" attributes
            try:
                _ns, prop_name = attr.split(style_ns + u'}')
            except ValueError:
                continue
            assert prop_name not in attrs
            attrs[prop_name] = child.get(attr)
    return attrs

def get_modified_style_props(new_style, old_style, style_ns):
    """
    compare 2 style nodes
    return : list with modified properties
    """
    modified_attrs = []
    new_attrs = get_style_properties(new_style, style_ns)
    old_attrs = get_style_properties(old_style, style_ns)
    # modified styles
    for attr in set(new_attrs.keys()).intersection(old_attrs.keys()):
        if new_attrs[attr] != old_attrs[attr]:
            modified_attrs.append({'name':attr,
                                   'old_value':old_attrs[attr],
                                   'new_value':new_attrs[attr]})
    # new styles
    for attr in set(new_attrs.keys()).difference(old_attrs.keys()):
        modified_attrs.append({'name':attr,
                               'new_value':new_attrs[attr],
                               'old_value':None})
    return modified_attrs

def automatic_style(name, family):
    """we try to filter some on the fly styles (WW8NumSt ...)"""
    # XXX semantics ?
    families = ("text", "paragraph")
    expr = r"^%s([0-9])+$" % family[0].upper()
    if family in families and re.match(expr, name):
        return True
    # automatic text style from WinWord transformation used in
    # XXX what to do with list definition WW8NumXXX
    # XXX is family == "text" sufficient
    # name.startswith("WW8Num") or re.match(r"^xl([0-9])+$", name):
    if family in ("table" , "table-cell", "table-column", "table-row"):
        return True
    return False

def get_doc_styles(styles_etree, filter_families=None):
    """
    get styles from styles.xml
    """
    styles = {}
    nsmap = styles_etree.nsmap
    for node in styles_etree.findall(".//{%(style)s}style" % nsmap):
        name = node.get('{%(style)s}name' % nsmap)
        family = node.get('{%(style)s}family' % nsmap)
        if filter_families and family in filter_families:
            continue
        #if family and is_style_automatic(name, family):
        #    continue
        styles[name + ':' + family] = node
    return styles


class UnsavedDocument(Exception): pass


class Checker(object):

    def __init__(self, lang, refstyle, writer, docwarning, xmlwarning,
                 category_levels=None):
        """
        :lang:
            i18n language
        :refstyle:
            reference styles.xml (as string)
        :writer:
            a callable to collect warnings
        :docwarning:
            a factory for document warnings
        :xmlwarning:
            a factory for xml warnings
        :category_levels:
            a dictionary containing logger level depending on category name
        """
        for ldir in (i18n.I18NPOPATH, '/usr/share/locale'):
            try:
                self._ = translation(domain='odtlib', localedir=ldir,
                                     languages=[lang]).ugettext
                break
            except:
                pass
        else:
            raise Exception('did not find .mo files')
        self.refstyle_etree = etree.fromstring(refstyle)
        self.w = writer
        self.docwarn = docwarning
        self.xmlwarn = xmlwarning
        self.category_levels = category_levels or {}
        self._reset()

    def get_category_info(self, category):
        """default level is warning (css class: war)"""
        name = category.lower().replace(' ', '-')
        name = unormalize(unicode(name))
        level = self.category_levels.get(name, "war")
        return (self._(category), level)

    def _reset(self):
        self.style_font_map = {}
        self.fonts_substitutions = {}
        self.warnings = []

    def write_warnings(self):
        for warning in self.warnings:
            self.w(warning.print_html())

    def write_unused_styles(self, unused_styles):
        """styles : are list of lists((name, family), )"""
        category, cat_level = self.get_category_info(_('Unused styles'))

        msg =(self._('Those styles will be replaced or lost if you choose to "fixe styles up".'),)
        headers = (self._('Styles'),)
        warning = self.xmlwarn((u', '.join([(pretty_style_name(s) + u' (%s)' % f)
                                            for s, f in unused_styles]),),
                               level=cat_level)
        self.warnings.append(self.docwarn(category, (warning,), headers=headers,
                                          help_msg=msg, level=cat_level))

    def get_font_stylefamily_map(self, content):
        """content is content.xml or styles.xml
        return default styles for font-families (paragraph, text, graphic, etc),
        if it exist"""
        font_stylefamily_maps = {}
        nsmap = content.nsmap
        for def_style in content.findall(".//{%(style)s}default-style" % nsmap):
            fontname = None
            stylefamily = def_style.get('{%(style)s}family' % nsmap)
            prop = def_style.find(".//{%(style)s}text-properties[@{%(style)s}font-name]" % nsmap)
            if prop is not None:
                fontname = prop.get('{%(style)s}font-name' % nsmap)
            self.style_font_map[stylefamily] = fontname
            if fontname is not None:
                font_stylefamily_maps[fontname] = stylefamily
        return font_stylefamily_maps

    def get_nodes_for_style(self, content, style):
        """return all text for nodes for a style in content.xml"""
        def get_text_for_nodes(nsmap, nodes, style):
            res = []
            for node in nodes:
                if node.tag == "{%(text)s}span" % nsmap:
                    text = self.get_text_for_span(node)
                else:
                    text = self.get_text_for_block(node, nsmap, style)
                if text :
                    res.append(text)
            return res
        nsmap =  content.nsmap
        nsmap.update({'c_fs': style})
        nodes = content.findall(".//*[@{%(text)s}style-name='%(c_fs)s']" % nsmap)
        return get_text_for_nodes(nsmap, nodes, style)

    def get_text_for_block(self, node, nsmap, style):
        """<text:p text:style-name="P11">
             Elle est en tous points semblable &#224; la m&#233;thode
             <text:span text:style-name="T26">&#8217;CONTRAINTE&#8217;</text:span>
               &#224; la diff&#233;rence pr&#232;s ...</text:p>
        """
        text = []
        if len(node.getchildren()) == 0:
            text_node = escaped_text(node)
            if text_node.strip():
                text.append(u'<strong>%s</strong>' % text_node)
        node_font = self.style_font_map.get(style)
        def recurse(node, text):
            if len(node.getchildren()) == 0:
                return
            text_node = process_text_node(node.text)
            if text_node.strip():
                text.append(u'<strong>%s </strong>' % text_node)
            for ch_node in node.iterchildren():
                ch_style = ch_node.get('{%(text)s}style-name' % nsmap)
                if ch_style and self.style_font_map.get(ch_style) != node_font:
                    text_node = process_text_node(ch_node.text)
                    if text_node.strip():
                        text.append(u'<span class="sober">%s </span>' % text_node)
                else:
                    text_node = process_text_node(ch_node.text)
                    if text_node.strip():
                        text.append(u'<strong>%s </strong>' % text_node)
                # now, ch_node children nodes
                recurse(ch_node, text)
                # tail of child node has the style of parent node ...
                text_node = process_text_node(ch_node.tail)
                if text_node.strip():
                    text.append(u'<strong>%s </strong>' % text_node)
            text_node = process_text_node(node.tail)
            if text_node.strip():
                text.append(u'<strong>%s </strong>' % text_node)
        recurse(node, text)
        return ''.join(text)

    def get_text_for_span(self, span):
        # XXX escaped_text provide a too large text ! (wtf ?)
        text = process_text_node(span.text)
        if not text:
            return u''
        para_text = unescaped_text(span.getparent())
        ind = para_text.find(text)
        assert ind != -1
        return (u'<span class="sober">%s</span> <strong>%s</strong> <span class="sober">%s</span>'  %
                (xml_escape(para_text[:ind]), xml_escape(text), xml_escape(para_text[ind+len(text):])))

    def collect_fonts(self, content, font_style_map, all_font_styles_map):
        """content : might be content.xml, or styles.xml
        return list of styles without fonts declaration"""
        # keep styles without explicit font declaration
        styles_without_fonts = []
        nsmap = content.nsmap
        # look up for style definitions
        for style in content.findall(".//{%(style)s}style" % nsmap):
            fontname = None
            fstyle = style.get('{%(style)s}name' % nsmap)
            ffamily = style.get('{%(style)s}family' % nsmap)
            prop_having_font = style.find(".//{%(style)s}text-properties[@{%(style)s}font-name]" % nsmap)
            if prop_having_font is not None:
                fontname = prop_having_font.get('{%(style)s}font-name' % nsmap)
                if fontname is not None:
                    self.style_font_map[fstyle] = fontname
                    font_style_map.setdefault(fontname, []).append({'style' : fstyle,
                                                                    'family': ffamily})
            else: # we lookup the font from a parent style :
                p_style = style.get("{%(style)s}parent-style-name" % nsmap)
                if p_style:
                    fontname = self.style_font_map.get(p_style, None)
                    if fontname:
                        self.style_font_map[fstyle] = fontname
                        all_font_styles_map.setdefault(fontname, []).append({'style' : fstyle,
                                                                             'family': ffamily})
            if fontname is None: # let's defer to the font family defined font
                fontname = self.style_font_map.get(ffamily)
                if fontname:
                    self.style_font_map[fstyle] = fontname
                    all_font_styles_map.setdefault(fontname, []).append({'style' : fstyle,
                                                                         'family': ffamily})
            if fontname is None: # many styles are graphics, ole or misc stuff related
                styles_without_fonts.append(fstyle)
        # look up in lists (style of bullets) XXX not important
        for def_list_node in content.findall(".//{%(text)s}list-style[@{%(style)s}name]" % nsmap):
            fstyle = def_list_node.get('{%(style)s}name' % nsmap)
            prop = def_list_node.find(".//{%(style)s}text-properties[@{%(style)s}font-name]" % nsmap)
            if prop is not None:
                fname = prop.get('{%(style)s}font-name' % nsmap)
                if fname:
                    self.style_font_map[fstyle] = fname

    # Checkers

    def lint(self, odtstream):
        """analyzes the document structure (a little) and styles
        and tells what's wrong about it"""
        self._reset()
        odt = StreamODFPackage(odtstream)
#         if 'layout-cache' not in odt.subelements():
#             raise UnsavedDocument
        content_etree = etree.fromstring(odt.data('content.xml'))
        content_etree.nsmap.update({'eq': u'éq'})
        styles_etree = etree.fromstring(odt.data('styles.xml'))
        styles_etree.nsmap.update({'eq': u'éq'})
        self.w('OpenOffice version', get_office_version(content_etree))
        #unused_cont_styles = get_unused_styles(content_etree)
        self.check_toc(content_etree)
        self.check_titles_maxdepth(content_etree)
        self.check_used_fonts(content_etree, styles_etree)
        self.check_table_sequences(content_etree)
        self.check_image_sequences(content_etree)
        # check styles
        self.check_new_styles(styles_etree, content_etree)
        # not here
        self.check_modified_styles(styles_etree)
        #self.write_unused_styles(get_unused_styles(styles_etree))
        self.write_warnings()

    def check_toc(self, content, toc_before_chapters=False):
        """Check the validity of the Table of contents"""
        category, cat_level = self.get_category_info(_("Table of contents"))
        nsmap = content.nsmap
        toc = content.findall('.//{%(text)s}table-of-content' % nsmap)
        warnings = []
        specs = [self._("The table of contents must be unique")]
        if toc_before_chapters:
            specs.append(self._("The table of contents must be placed before the first header"))
        headers = (self._('Errors'),)

        if not toc:
            warning = (self._("This document contains no table of contents"),)
            warnings.append(self.xmlwarn(warning, level=cat_level))
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              specs=specs, level=cat_level))
            return
        depth_error = self.check_depth_toc(toc)
        if depth_error is not None:
            warnings.append(depth_error)
        for i, table in enumerate(toc):
            title = table.find('.//{%(text)s}index-title' % nsmap)
            if title is None:
                warning = (self._("No automatically generated title found for the table of contents number %d") % i,)
                warnings.append(self.xmlwarn(warning, level=cat_level))
        # toc node must be placed before the first h node
        if toc_before_chapters:
            toc_node = False
            for child in content.find('.//{%(office)s}text' % nsmap).iterchildren():
                if child.tag == "{%(text)s}table-of-content" % nsmap:
                    toc_node = True
                if child.tag == "{%(text)s}h" % nsmap:
                    if not toc_node:
                        warning = (self._("The table of contents must be placed before the first header"),)
                        warnings.append(self.xmlwarn(warning, level=cat_level))
                        break
        if warnings:
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              specs=specs, level=cat_level))

    def check_depth_toc(self, toc):
        category, cat_level = self.get_category_info(_("Depth of table of contents"))

        if len(toc) > 1 :
            warning = (self._("This document contains %d tables of contents") % len(toc),)
            return self.xmlwarn(warning, level=cat_level)

    def check_titles_maxdepth(self, content):
        """
        The text:outline-level attribute of text:h nodes determines
        the level of the heading, starting with 1. Headings without a
        level attribute are assumed to be at level 1
        """
        category, cat_level = self.get_category_info(_("Headers"))
        nsmap = content.nsmap
        warnings = []

        for title_node in content.findall('.//{%(text)s}h' % nsmap):
            level = int(title_node.get("{%(text)s}outline-level" % nsmap,  1))
            if level > 4 :
                title = escaped_text(title_node)
                warning = (self._("Unauthorized level %d") % level, title)
                warnings.append(self.xmlwarn(warning, level=cat_level))
        if len(warnings) > 0:
            headers = (self._('Errors'), self._("Text"))
            specs = (self._("The table of contents must be placed before the first header"),
                     self._("The table of contents must be unique"))
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              specs=specs, level=cat_level))

    def check_used_fonts(self, content, styles):
        """
        check all fonts used in content.xml and styles.xml
        we dont mind asian and complex fonts (style:font-name-complex and style:font-name-asian)
        """
        category, cat_level = self.get_category_info(_('Fonts'))

        def fonts_warnings(content, font_style_map, font_stylefamily_maps,
                           font_families, show_nodes=False, msg=()):
            """optional parameters:
               show_all              : show all fonts (if False, shows only fonts not contained in authorized FONTS)
               show_nodes            : if False - only write style names, write style names and text otherwise
            """
            warnings = []
            font_substitution = {}
            # default styles  : highlight font / font-family mapping
            for font, style in font_stylefamily_maps.iteritems():
                if style in EXCLUDED_STYLE:
                    continue
                families = font_families[font]
                show_font = not (set(families).intersection(ALLOWED_FONTS)) # XXX correctness
                if show_font:
                    warning = (', '.join(families), self._('default font for %ss') % style)
                    warnings.append(self.xmlwarn(warning, level=cat_level))
            # others
            for font, styles in font_style_map.iteritems():
                families = font_families[font]
                show_font = not (set(families).intersection(ALLOWED_FONTS)) # XXX correctness
                if not show_nodes:
                    if show_font :
                        warnings.append(self.xmlwarn((', '.join(families),
                                                      ', '.join(pretty_style_name(style['style'])
                                                                for style in styles)),
                                                     level=cat_level))
                else: # Must provide font substitution manually
                    cfont, exact_match = canonical_font(font)
                    if cfont is not None:
                        if not exact_match:
                            font_substitution[font] = cfont
                        continue
                    font_substitution[font] = None
                    for style in styles:
                        if show_font: # show_block
                            nodes = self.get_nodes_for_style(content, style['style'])
                            if not nodes:
                                continue
                            nodes_text = ''.join(nodes).strip()
                            font_note = self._('%(font)s (inline style: %(style)s, family: %(family)s)') %\
                                {'font' : font, 'style' : style['style'], 'family' : style['family']}
                            if nodes_text:
                                warnings.append(self.xmlwarn((font_note, '<br/>'.join(nodes)),
                                                             level=cat_level))
            return font_substitution, warnings

        self.style_font_map['text'] = self.style_font_map.get('paragraph', 'UNKNOWN BASE FONT')
        all_font_style_map = {}
        # check styles.xml
        styles_font_style_map = {}
        self.collect_fonts(styles, styles_font_style_map, all_font_style_map)
        # check content.xml
        content_font_style_map = {}
        self.collect_fonts(content, content_font_style_map, all_font_style_map)

        # font families
        font_families = get_font_families(content, styles)
        # write styles which be automatically replaced
        msg = (self._('Those fonts will be automatically replaced if you choose to "fixe styles up".'),)
        font_subst, warnings = fonts_warnings(styles, styles_font_style_map, self.get_font_stylefamily_map(styles),
                                              font_families, msg=msg)
        self.fonts_substitutions.update(font_subst)
        if warnings:
            specs = (self._('Authorized fonts are : %s') % ", ".join(ALLOWED_FONTS),)
            headers=(self._('Font'), self._('Styles using this font'))
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              help_msg=msg, specs=specs, level=cat_level))
        # write styles to be cleaned
        msg = (self._('Following text blocks use fonts for which you must choose a substitution'),)
        font_subst, warnings = fonts_warnings(content, content_font_style_map, self.get_font_stylefamily_map(content),
                                              font_families, show_nodes=True, msg=msg)
        self.fonts_substitutions.update(font_subst)
        if warnings:
            specs = ('')
            headers=(self._('Font'), self._('Text blocks using this font'))
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              help_msg=msg, level=cat_level))

    def check_table_sequences(self, content):
        """check tables without legends"""
        category, cat_level = self.get_category_info(_('Tables legends'))
        nsmap = content.nsmap
        warnings = []

        for table_node in content.findall('.//{%(table)s}table' % nsmap):
            table_name = table_node.get('{%(table)s}name'% nsmap)
            table_text = unescaped_text(table_node)
            next_node = table_node.getnext()
            if next_node is None:
                table_text = xml_escape(cut_text(table_text, 500))
                warning = (self._('No automatically generated legend found for %s') % table_name,  table_text)
                warnings.append(self.xmlwarn(warning, level=cat_level))
                continue
            legend = next_node.find( ".//{%(text)s}sequence" % nsmap)
            if legend is None:
                table_text = xml_escape(cut_text(table_text, 500))
                warning = (self._('No automatically generated legend found for %s') % table_name,  table_text)
                warnings.append(self.xmlwarn(warning, level=cat_level))
            else:
                legend_name = legend.get('{%(text)s}name' % nsmap)
                if legend_name != 'Table':
                    warning = (self._('Wrong legend name for %s') % legend_name,)
                    warnings.append(self.xmlwarn(warning, level=cat_level))
        if warnings:
            specs = (self._("Tables legends must respect the following format : "
                            "'Tableau' followed by the chapter number and the table indice : (ex:'Tableau 1.1 -2')"),)
            headers = (self._('Error'), self._('Table text'), )
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              specs=specs, level=cat_level))


    def check_image_sequences(self, content):
        """check images without legends
        XXX : shell we add missing labels? """
        category, cat_level = self.get_category_info(_('Images legends'))
        nsmap = content.nsmap
        warnings = []

        for image in content.findall('.//{%(draw)s}image' % nsmap):
            p_image = image.getparent()
            image_name = p_image.get('{%(draw)s}name'% nsmap)
            legend = p_image.find('.//{%(text)s}sequence' % nsmap)
            if legend is None:
                # do not take account of ole obj
                if p_image.find('.//{%(draw)s}object' % nsmap) is None and \
                    p_image.find('.//{%(draw)s}object-ole' % nsmap) is  None:
                    warning = (self._('No automatically genereted legend found for %s') % image_name,)
                    warnings.append(self.xmlwarn(warning, level=cat_level))
        if warnings:
            headers = (self._('Error'),)
            specs = (self._('Images legends must respect the following format :  '
                       "'Images' followed by the chapter number and the table indice : (ex:'Image 1.1 -1')."),)
            self.warnings.append(self.docwarn(category, warnings, headers=headers,
                                              specs=specs, level=cat_level))

    def check_new_styles(self, docstyles_etree,  content_etree):
        """compare a document and reference styles.xml and find new_styles in
        the document
        XXX we need to track deviations to the existing, correct styles """
        category, cat_level = self.get_category_info(_('New styles'))
        docstyles = get_doc_styles(docstyles_etree, filter_families=('text', ))
        refstyles = get_doc_styles(self.refstyle_etree, filter_families=('text',))
        warnings = []

        for style in set(docstyles.keys()).difference(refstyles.keys()):
            style_name, style_family  = style.split(":")
            nodes = self.get_nodes_for_style(content_etree, style_name)
            style_name = pretty_style_name_from_node(docstyles[style], docstyles_etree.nsmap)
            style_name += u" (" + style_family + ")"
            if len(nodes) > 0:
                warnings.append(self.xmlwarn((style_name, self._('This style is not used')),
                                             level=cat_level))
            else:
                warnings.extend([self.xmlwarn((style_name, node),
                                              level=cat_level) for node in nodes])
        if warnings:
            msg = (self._('Those styles will be lost or replaced '
                          'if you choose to "fixe styles up".'),)
            headers = (self._('Style (style family)'), self._('Text using this style'))
            warnings.append(self.docwarn(category, warnings, headers=headers,
                                         help_msg=msg, level=cat_level))
        # to do : search text with those styles

    def check_modified_styles(self, docstyles_etree):
        """
        compare document and reference styles.xml and find modified_styles
        in the document
        """
        category, cat_level = self.get_category_info(_('Modified styles'))
        # search for modified styles
        docstyles = get_doc_styles(docstyles_etree, filter_families=('text', ))
        refstyles = get_doc_styles(self.refstyle_etree, filter_families=('text',))
        warnings = []
        modified_styles = {}
        value_str = u'%(name)s : %(new_value)s <span class="sober"> / </span> %(old_value)s'

        for style in set(docstyles.keys()).intersection(refstyles.keys()):
            style_name, style_family  = style.split(":")
            modified_attrs = get_modified_style_props(docstyles[style], refstyles[style],
                                                       docstyles_etree.nsmap['style'])
            if modified_attrs:
                style_name = pretty_style_name_from_node(docstyles[style], docstyles_etree.nsmap)
                style_name += u" (" + style_family + ")"
                for attr in modified_attrs:
                    values = value_str % attr
                    modified_styles.setdefault(style_name, []).append(values)
        for style, value in modified_styles.iteritems():
            warnings.append(self.xmlwarn((style , value), level=cat_level))
        if warnings:
            # Outils > Options... > OpenOffice.org.Writer > Général > Unité de mesure
            specs = (self._('Some differences in styles (in/pt/cm) may be caused by the diffrence '
                            'in measurement unit settings. Choose '
                            '"Tools > Options... > OpenOffice.org.Writer > General > Measurement unit " '
                            'to set the right unit (cm).'), )
            msg = (self._('Those modifications will be lost '
                          'if you choose to "fixe styles up".'),)
            headers = (self._("Style (style family)"), self._('Attribute :  new value vs old value'))
            warnings.append(self.docwarn(category, warnings, headers=headers,
                                         specs=specs, help_msg=msg, level=cat_level))
