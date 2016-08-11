from django.conf import settings
import re
from django.forms.fields import CharField
from django.db import models
from ideia_summernote.widget import SummernoteWidget
import bleach


class SummernoteFormField(CharField):

    def __init__(self, editor_conf='default', load_init=True, async=False, *args, **kwargs):

        kwargs.update({'widget': SummernoteWidget(editor_conf=editor_conf, load_init=load_init, async=async)})
        super(SummernoteFormField, self).__init__(*args, **kwargs)

    def default_tag_map(self):

        default_attrs = ['style', 'line-height']

        map = {
            'bold': {
                'b': default_attrs,
            },
            'italic': {
                'i': default_attrs
            },
            'underline': {
                'u': default_attrs
            },
            'superscript':{
                'sub': default_attrs
            },
            'subscript': {
                'sup': default_attrs
            },
            'strikethrough': {
                'strike': default_attrs
            },
            'fontsize': {
                'span': default_attrs
            },
            'ul': {
                'ul': default_attrs,
                'li': default_attrs
            },
            'ol': {
                'ol': default_attrs,
                'li': default_attrs
            },
            'picture': {
                'img': default_attrs + ['src']
            }
        }

        return map

    def clean(self, value):
        value = super(SummernoteFormField, self).clean(value)
        try:
            enabled_tags = self.get_editor().get('enabledTags', {})
            toolbar_conf = self.get_editor().get('toolbar', [])
            enabled_styles = self.get_editor().get('enabledStyles', {})
            default_map = self.default_tag_map()

            enabled_keys = []

            for tconf_items in toolbar_conf:
                t_item = tconf_items[1] if len(tconf_items) > 0 else None
                if not t_item:
                    continue
                [enabled_keys.append(i) for i in t_item]

            enabled_keys = list(set(enabled_keys))

            attrs = {}
            tags = []

            for key, item in default_map.items():
                if key not in enabled_keys:
                    continue

                [tags.append(i) for i in item.keys()]
                attrs.update(item)

            tags = list(set(tags))

            for etag, eattrs in enabled_tags.items():
                tags.append(etag)
                attrs.update({'%s' % etag: eattrs})

            value = bleach.clean(value, tags=tags, attributes=attrs, styles=enabled_styles, strip=True)
        except Exception, e:
            print e.message

        return value

    def get_editor(self):
        return self.widget.get_editor()


class SummernoteField(models.TextField):

    def __init__(self, editor_conf='default', load_init=True, async=False, *args, **kwargs):
        self.editor_conf = editor_conf
        self.load_init=load_init
        self.async=async
        super(SummernoteField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):

        defaults = {
            'form_class':  SummernoteFormField,
            'editor_conf': self.editor_conf,
            'load_init': self.load_init,
            'async': self.async
        }

        defaults.update(kwargs)
        return super(SummernoteField, self).formfield(**defaults)