from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from lxml import etree
from lxml.etree import HTMLParser, ParseError

def colorize_node(node, formatter, lexer):
    html_hilite = highlight(node.text, lexer, formatter)

    if html_hilite:
        # when building the html tree in lxml it automatically embeds the html
        # in html/body tags, so we need to travel back to the stuff we want
        code_tree = etree.fromstring(html_hilite, HTMLParser())

        # also possible this could be a table, hence the node()
        div_tree = code_tree.xpath('/html/body/node()[1]')[0]

        # we need to find what tags to replace
        # if this is a <code> tag by itself, just replace the text
        # if it is a <code> tag that is the child of a <pre> tag, replace the pre node
        # if it is a <pre> tag by itself, just replace the node
        if node.tag == 'code':
            if node.getparent().tag == 'pre':  # <pre><code> tags
                parent = node.getparent().getparent()
                parent.replace(node.getparent(), div_tree)
            else:  # <code> tag only
                parent = node.getparent()
                parent.replace(node, div_tree)
        else:  # <pre> tag only
            parent = node.getparent()
            parent.replace(node, div_tree)


def colorizer(plain_html, default='', style='default', border='', inline=False, linenos=False):
    tree = etree.fromstring(plain_html, HTMLParser())
    formatter = HtmlFormatter(style=style, linenos=linenos, cssstyles=border, 
                              noclasses=inline, cssclass='colorize')

    # iterate over all code tags and pre tags who do not have
    # a nested code tag
    converted = 0
    log = []
    for code_elem in tree.xpath('//code | //pre[not(code)]'):
        found_lexer = False
        if not code_elem.text:
            continue

        # lets remove all nodes and gather the code underneath this element
        # as a text node
        text = code_elem.xpath('.//text()')
        for elem in code_elem.iterdescendants(etree.Element):
            elem.getparent().remove(elem)
        code_elem.text = str.join('', text)

        if code_elem.attrib.has_key('class') and code_elem.attrib['class']:
            try:
                log.append('Using lexer [%s] on tag <%s> @ line %d' % (code_elem.attrib['class'], code_elem.tag, code_elem.sourceline))
                # throws an exception if lexer is not found
                lexer = get_lexer_by_name(code_elem.attrib['class'])
                colorize_node(code_elem, formatter, lexer)
                found_lexer = True
                converted += 1
            except Exception as e:
                log.append('Error on tag <%s> @ line %d :: %s' % (code_elem.tag, code_elem.sourceline, e))

        # if finding the lexer by tag and class name fails, we'll fall to the default
        # only if the code contains multiple lines (this tries to avoid inlined code)
        if not found_lexer and default and len(str.splitlines(code_elem.text)) > 1:
            try:
                log.append('Using default lexer [%s] on tag <%s> @ line %d' % (default, code_elem.tag, code_elem.sourceline))
                lexer = get_lexer_by_name(default)
                colorize_node(code_elem, formatter, lexer)
                found_lexer = True
                converted += 1
            except Exception as e:
                log.append('Error on tag <%s> @ line %d :: %s' % (code_elem.tag, code_elem.sourceline, e))
                continue

        # lastly, if there is no default defined, we'll try to guess the lexer.
        # this seems to be hit or miss
        if not found_lexer and not default and len(str.splitlines(code_elem.text)) > 1:
            try:
                log.append('No default lexer, attempting to guess <%s> @ line %d' (code_elem.tag, code_elem.sourceline))
                # throws an exception on failure
                lexer = guess_lexer(code_elem.text)
                log.append('Lexer guess succeeded, using [%s] on tag <%s> @ line %d' (lexer.alias[0], code_elem.tag, code_elem.sourceline))
                colorize_node(code_elem, formatter, lexer)
                converted += 1
            except Exception as e:
                log.append('Error on tag <%s> @ line %d :: %s' % (code_elem.tag, code_elem.sourceline, e))
                continue

    script = ''
    if converted > 0:
        try:
            script = formatter.get_style_defs('.colorize')

            # if it's not inline we need to add the script to the style section
            if not inline:
                style_tag = tree.xpath('/html/head/style')
                if style_tag:
                    style_tag[0].text += script
                else:
                    # if the <style> tag doesn't exist we need to create it
                    # this might also mean we need to create the <head> tag
                    head_tag = tree.xpath('/html/head')
                    head_tag = head_tag[0] if head_tag else None
                    if not head_tag:
                        tree.insert(0, etree.Element('head'))
                        head_tag = tree.find('head')
                    style = etree.Element('style')
                    style.text = script
                    head_tag.append(style)

            html_result = etree.tostring(tree, method='html', pretty_print=True)
        except Exception as e:
            log.append('Error creating style script')
    else:
        html_result = html_hilite

    return (converted > 0), log, converted, html_result, script
