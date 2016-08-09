from django.forms.fields import CharField
from django.db import models
from ideia_summernote.widget import SummernoteWidget


class SummernoteFormField(CharField):


    def __init__(self, editor_conf='default', load_init=True, async=False, plugins=None, *args, **kwargs):

        kwargs.update({'widget': SummernoteWidget(editor_conf=editor_conf, load_init=load_init, async=async, plugins=plugins)})
        super(SummernoteFormField, self).__init__(*args, **kwargs)


class SummernoteField(models.TextField):

    def formfield(self, **kwargs):
        self.editor_conf = kwargs.pop("editor_conf", "default")

        defaults = {
            'form_class':  SummernoteFormField,
            'editor_conf': self.editor_conf
        }

        defaults.update(kwargs)
        return super(SummernoteField, self).formfield(**defaults)