# -*- coding: utf-8 -*-
import re
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


class NavSelectedNode(template.Node):
    def __init__(self, strict, with_class, klass, urls):
        self.strict = strict
        self.with_class = with_class
        self.klass = klass
        self.urls = urls

    def render(self, context):
        from dj_kits.utils.templates import parse_bool_value

        def resolve_var(x):
            if x is None:
                return None
            else:
                try:
                    return template.Variable(x).resolve(context)
                except template.VariableDoesNotExist:
                    # Django seems to hide those; we don't want to expose
                    # them either, I guess.
                    raise

        strict = parse_bool_value(resolve_var(self.strict), 'strict')
        if strict is None:
            strict = True

        with_class = parse_bool_value(resolve_var(self.with_class), 'with_class')
        if with_class is None:
            with_class = True

        klass = resolve_var(self.klass)
        if klass is None:
            klass = 'active'

        try:
            path = context['request'].path
        except KeyError:
            path = ''

        for url in self.urls:
            pValue = template.Variable(url).resolve(context)
            if (pValue == '/' or pValue == '') and not (path  == '/' or path == ''):
                return ""
            if path == pValue or (not strict and pValue in path):
                if with_class:
                    attr = ' class="%s"'
                else:
                    attr = ' %s'
                return attr % klass
        return ""


@register.tag
def current_nav(parser, token):

    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag

    args = args[1:]

    strict = None
    with_class = None
    klass = None
    urls = []

    for arg in args:
        arg = arg.split('=', 1)
        if len(arg) == 1:
            urls.append(arg[0])
        else:
            if arg[0] == 'strict':
                strict = arg[1]
            elif arg[0] == 'with_class':
                with_class = arg[1]
            elif arg[0] == 'class':
                klass = arg[1]
            else:
                raise template.TemplateSyntaxError, "%r tag unknow argument %s" % (template_tag, arg[0])

    if not urls:
        raise template.TemplateSyntaxError, "%r tag requires at least one url argument" % template_tag

    return NavSelectedNode(strict, with_class, klass, urls)


class DefineNode(template.Node):
    def __init__(self, var, name):
        self.var = var
        self.name = name

    def __repr__(self):
        return "<DefineNode>"

    def render(self, context):
        context.dicts[0][self.name] = self.var
        return ''


@register.tag
def define(parser, token):
    """
    Adds a name to the context for referencing an arbitrarily defined string.

    For example:

        {% define "my_string" as my_string %}

    Now anywhere in the template:

        {{ my_string }}
    """
    bits = list(token.split_contents())
    if (len(bits) != 4 or bits[2] != "as") or \
        not (bits[1][0] in ('"', "'") and bits[1][-1] == bits[1][0]):
        raise template.TemplateSyntaxError("%r expected format is '\"string\" as name'" % bits[0])
    else:
        value = bits[1][1:-1]
    name = bits[3]

    return DefineNode(value, name)


@register.filter
def tojson(value):
    """
    Turns value to JSON format.

    Usage:
        {{ value|tojson }}
    """
    import json
    from django.utils.functional import Promise

    if hasattr(value, '__json__'):
        value = value.__json__()
    elif hasattr(value, 'to_json'):
        value = value.to_json()

    if isinstance(value, Promise):
        if hasattr(value, '_proxy____unicode_cast'):
            value = value._proxy____unicode_cast()
        elif hasattr(value, '_proxy____text_cast'):
            value = value._proxy____text_cast()

    return mark_safe(json.dumps(value).replace('</', '<\\/'))


@register.filter
def paragraphs(value):
    """
    Turns paragraphs delineated with newline characters into
    paragraphs wrapped in <p> and </p> HTML tags.

    Usage:
        {{ string|paragraphs }}
    """
    paras = re.split(r'[\r\n]+', value)
    paras = ['<p>%s</p>' % p.strip() for p in paras]
    return mark_safe('\n'.join(paras))


@register.filter
def timesincesmart(value, arg=None):
    """Formats a date as the time since that date (twitter like)."""
    from dj_kits.utils.timesince import timesince
    if not value:
        return u''
    try:
        if arg:
            return timesince(value, arg)
        return timesince(value)
    except (ValueError, TypeError):
        return u''
timesincesmart.is_safe = False


@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = unicode(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Join the words and return
    return value + '...'


@register.filter
def urlizesmart(value):
    """Converts URLs in plain text into clickable links."""
    from dj_kits.utils.html import urlizesmart as urlizesmart_impl
    return mark_safe(urlizesmart_impl(value))



"""

    Most of this code was written by Miguel Araujo
    https://gist.github.com/893408

"""

def verbatim_tags(parser, token, endtagname):
    """
    Javascript templates (jquery, handlebars.js, mustache.js) use constructs like:

    ::

        {{if condition}} print something{{/if}}

    This, of course, completely screws up Django templates,
    because Django thinks {{ and }} means something.

    The following code preserves {{ }} tokens.

    This version of verbatim template tag allows you to use tags
    like url {% url name %}. {% trans "foo" %} or {% csrf_token %} within.
    """
    text_and_nodes = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == endtagname:
            break

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('{{')
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_TEXT:
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_BLOCK:
            try:
                command = token.contents.split()[0]
            except IndexError:
                parser.empty_block_tag(token)

            try:
                compile_func = parser.tags[command]
            except KeyError:
                parser.invalid_block_tag(token, command, None)
            try:
                node = compile_func(parser, token)
            except template.TemplateSyntaxError, e:
                if not parser.compile_function_error(token, e):
                    raise
            text_and_nodes.append(node)

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('}}')

    return text_and_nodes


class VerbatimNode(template.Node):
    """
    Wrap {% verbatim %} and {% endverbatim %} around a
    block of javascript template and this will try its best
    to output the contents with no changes.

    ::

        {% verbatim %}
            {% trans "Your name is" %} {{first}} {{last}}
        {% endverbatim %}
    """
    def __init__(self, text_and_nodes):
        self.text_and_nodes = text_and_nodes

    def render(self, context):
        output = ""
        # If its text we concatenate it, otherwise it's a node and we render it
        for bit in self.text_and_nodes:
            if isinstance(bit, basestring):
                output += bit
            else:
                output += bit.render(context)
        return output


@register.tag
def verbatim(parser, token):
    text_and_nodes = verbatim_tags(parser, token, 'endverbatim')
    return VerbatimNode(text_and_nodes)


@register.tag
def verbatimsmart(parser, token):
    text_and_nodes = verbatim_tags(parser, token, 'endverbatimsmart')
    return VerbatimNode(text_and_nodes)


@register.tag
def query_string(parser, token):
    """
    Allows you too manipulate the query string of a page by adding and removing keywords.
    If a given value is a context variable it will resolve it.
    Based on similiar snippet by user "dnordberg".

    requires you to add:

    TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    )

    to your django settings.

    Usage:
    http://www.url.com/{% query_string "param_to_add=value, param_to_add=value" "param_to_remove, params_to_remove" %}

    Example:
    http://www.url.com/{% query_string "" "filter" %}filter={{new_filter}}
    http://www.url.com/{% query_string "page=page_obj.number" "sort" %}

    """
    try:
        tag_name, add_string,remove_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    if not (add_string[0] == add_string[-1] and add_string[0] in ('"', "'")) or not (remove_string[0] == remove_string[-1] and remove_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    add = string_to_dict(add_string[1:-1])
    remove = string_to_list(remove_string[1:-1])

    return QueryStringNode(add,remove)


class QueryStringNode(template.Node):
    def __init__(self, add,remove):
        self.add = add
        self.remove = remove

    def render(self, context):
        p = {}
        for k, v in context["request"].GET.items():
            p[k]=v
        return get_query_string(p,self.add,self.remove,context)

def get_query_string(p, new_params, remove, context):
    """
    Add and remove query parameters. From `django.contrib.admin`.
    """
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if k in p and v is None:
            del p[k]
        elif v is not None:
            p[k] = v

    for k, v in p.items():
        try:
            p[k] = template.Variable(v).resolve(context)
        except:
            p[k]=v

    return mark_safe('?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in p.items()]).replace(' ', '%20'))

# Taken from lib/utils.py
def string_to_dict(string):
    kwargs = {}

    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            kw, val = arg.split('=', 1)
            kwargs[kw] = val
    return kwargs


def string_to_list(string):
    args = []
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '': continue
            args.append(arg)
    return args