from django.forms.fields import CharField
from django.db import models
from ideia_summernote.widget import SummernoteWidget


class SummernoteFormField(CharField):


    def __init__(self, editor_conf='default', load_init=True, async=False, *args, **kwargs):

        kwargs.update({'widget': SummernoteWidget(editor_conf=editor_conf, load_init=load_init, async=async)})
        super(SummernoteFormField, self).__init__(*args, **kwargs)

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