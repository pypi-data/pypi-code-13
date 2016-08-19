import json
from django.conf import settings
from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe
from default import SUMMERNOTE_DEFAULT_CONFIG


class SummernoteWidget(forms.Textarea):

    def _media(self):
        django_jquery_adapter = settings.STATIC_URL + 'js/django-jquery-adapter.js'
        js = (django_jquery_adapter,) + self.assets.get('js')
        if self.load_init:
            js+= (settings.STATIC_URL + 'js/summernote-init.js',)
        return forms.Media(css=self.assets.get('css'),
                           js=js)
    media = property(_media)


    def get_editor(self):
        return self.editor_conf


    def __init__(self, editor_conf=None, load_init=True, async=None, *args, **kwargs):

        self.load_init = load_init
        self.async = async
        self.general_config = getattr(settings, 'SUMMERNOTE_CONFIG', SUMMERNOTE_DEFAULT_CONFIG)
        self.editors = self.general_config.get('editors')
        self.editor_conf=self.editors.get(editor_conf or 'default', self.editors.get('default'))


        self.assets = self.general_config.get('assets', SUMMERNOTE_DEFAULT_CONFIG.get('assets'))


        super(SummernoteWidget, self).__init__(*args, **kwargs)


    def render(self, name, value, attrs=None):
        return mark_safe(render(None, 'ideia_summernote/default.html', { 'self': self,
                                                                        'name': name,
                                                                         'value': value,
                                                                        'async': self.async,
                                                                        'config': json.dumps(self.editor_conf),
                                                                         'attrs': attrs

                                                                        }).content)