#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from django import template
from django.template.defaulttags import URLNode, url
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.tag
def smarturl(parser, token):
    validator = url(parser, token)
    return SmartURLNode(validator.view_name, validator.args, validator.kwargs, validator.asvar)



class SmartURL(str):
    """
    This is a wrapper class that allows us to attach attributes to regular
    unicode strings.
    """
    pass


class SmartURLNode(URLNode):

    # def __init__(self, view_name, args, kwargs, asvar):
    #     super(SmartURLNode, self).__init__(view_name, args, kwargs, asvar)
    #     self.crap = 'test'

    def render(self, context):

        # Loosely based off of https://www.silviogutierrez.com/blog/smarter-django-url-tag/ and
        # http://www.turnkeylinux.org/blog/django-navbar

        # Get the view name and the current url from the request object
        resolved_view_name = self.view_name.resolve(context)
        request_url = context.get('request', None).path

        # Resolve the
        try:
            resolved_url = reverse(resolved_view_name)
        except NoReverseMatch:
            return ''

        # Save the resolved url string into the SmartURL object
        rendered = SmartURL(resolved_url)

        # Add active and active_root properties
        if resolved_url == request_url:
            rendered.active = ' selected'
        else:
            rendered.active = ''

        parent_url = '/'.join(resolved_url.split('/')[:-1])

        if request_url.startswith(parent_url):
            rendered.active_root = ' button-selected'
        else:
            rendered.active_root = ''

        # Assign the SmartURL instance back into the context and we're done.
        # As this is an assignment use, return an empty string.
        context[self.asvar] = rendered

        return ''


