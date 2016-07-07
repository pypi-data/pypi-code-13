# vim: set fileencoding=utf-8 :
"""
permissionif templatetag
"""
import django
from django import template
from django.template import TemplateSyntaxError
from django.template import VariableDoesNotExist
from django.template.smartif import infix
from django.template.smartif import IfParser
from django.template.smartif import OPERATORS
from django.template.defaulttags import Node
from django.template.defaulttags import NodeList
from django.template.defaulttags import TemplateLiteral
from simple_permissions.conf import settings
from simple_permissions.templatetags.patch import IfNode
from simple_permissions.templatetags.patch import parser_patch


register = template.Library()


def of_operator(context, x, y):
    """
    'of' operator of permission if

    This operator is used to specify the target object of permission
    """
    return x.eval(context), y.eval(context)

def has_operator(context, x, y):
    """
    'has' operator of permission if

    This operator is used to specify the user object of permission
    """
    user = x.eval(context)
    perm = y.eval(context)
    if isinstance(perm, (list, tuple)):
        perm, obj = perm
    else:
        obj = None
    return user.has_perm(perm, obj)

# Add 'of' and 'has' operator to existing operators
EXTRA_OPERATORS = {
    'of': infix(20, of_operator),
    'has': infix(10, has_operator),
}
EXTRA_OPERATORS.update(OPERATORS)
for key, op in EXTRA_OPERATORS.items():
    op.id = key


class PermissionIfParser(IfParser):
    """Permission if parser"""
    OPERATORS = EXTRA_OPERATORS
    """use extra operator"""

    def translate_token(self, token):
        try:
            # use own operators instead of builtin operators
            op = self.OPERATORS[token]
        except (KeyError, TypeError):
            return self.create_var(token)
        else:
            return op()

class TemplatePermissionIfParser(PermissionIfParser):
    error_class = TemplateSyntaxError

    def __init__(self, parser, *args, **kwargs):
        self.template_parser = parser
        super(TemplatePermissionIfParser, self).__init__(*args, **kwargs)

    def create_var(self, value):
        return TemplateLiteral(self.template_parser.compile_filter(value), value)


@register.tag('permission')
def do_permissionif(parser, token):
    """
    Permission if templatetag

    Examples
    --------
    ::

        {% if user has 'blogs.add_article' %}
            <p>This user have 'blogs.add_article' permission</p>
        {% elif user has 'blog.change_article' of object %}
            <p>This user have 'blogs.change_article' permission of {{object}}</p>
        {% endif %}

        {# If you set 'SIMPLE_PERMISSIONS_REPLACE_BUILTIN_IF = False' in settings #}
        {% permission user has 'blogs.add_article' %}
            <p>This user have 'blogs.add_article' permission</p>
        {% elpermission user has 'blog.change_article' of object %}
            <p>This user have 'blogs.change_article' permission of {{object}}</p>
        {% endpermission %}

    """
    # patch parser for django 1.3.1
    parser = parser_patch(parser)

    bits = token.split_contents()
    ELIF = "el%s" % bits[0]
    ELSE = "else"
    ENDIF = "end%s" % bits[0]

    # {% if ... %}
    bits = bits[1:]
    condition = do_permissionif.Parser(parser, bits).parse()
    nodelist = parser.parse((ELIF, ELSE, ENDIF))
    conditions_nodelists = [(condition, nodelist)]
    token = parser.next_token()

    # {% elif ... %} (repeatable)
    while token.contents.startswith(ELIF):
        bits = token.split_contents()[1:]
        condition = do_permissionif.Parser(parser, bits).parse()
        nodelist = parser.parse((ELIF, ELSE, ENDIF))
        conditions_nodelists.append((condition, nodelist))
        token = parser.next_token()

    # {% else %} (optional)
    if token.contents == ELSE:
        nodelist = parser.parse((ENDIF,))
        conditions_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% endif %}
    assert token.contents == ENDIF

    return IfNode(conditions_nodelists)
do_permissionif.Parser = TemplatePermissionIfParser

# To replace builtin if
if django.VERSION >= (1, 4):
    def replace_builtin_if(replace=False):
        if replace:
            OPERATORS.update({
                'has': EXTRA_OPERATORS['has'],
                'of': EXTRA_OPERATORS['of'],
            })
        else:
            # remove of, has from OPERATORS
            OPERATORS.pop('of', None)
            OPERATORS.pop('has', None)
else:
    # Django 1.3 and earlier use a different if model
    # So re-register if
    def replace_builtin_if(replace):
        if replace:
            register.tag('if', do_permissionif)
        else:
            from django.template.defaulttags import do_if
            register.tag('if', do_if)

replace_builtin_if(settings.SIMPLE_PERMISSIONS_REPLACE_BUILTIN_IF)
