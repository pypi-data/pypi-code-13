# -*- coding: utf-8 -*-
from django.forms.util import ErrorList


def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )


def json_to_errors(errors, form=None, error_class=ErrorList):
    """
    Convert a JSON error to Form error::
    """
    _errors = form.errors if form else {}
    for name, v in errors.items():
        _errors[name] = error_class(v)
    return _errors


class FormBaseMixin(object):

    error_text_inline = True
    form_action = '.'
    form_class = ''
    form_inputs = []
    form_method = 'post'

    def get_form_method(self):
        return self.form_method

    def get_form_action(self):
        return self.form_action

    def get_form_class(self):
        return self.form_class

    def get_form_inputs(self):
        return self.form_inputs

    def get_layout(self, helper):
        return helper.build_default_layout(self)

    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            from crispy_forms.helper import FormHelper
            self._helper = FormHelper()
            self._helper.error_text_inline = self.error_text_inline
            self._helper.form_action = self.get_form_action()
            self._helper.form_class = self.get_form_class()
            self._helper.form_method = self.get_form_method()

            for input in self.get_form_inputs():
                self._helper.add_input(input)

            self._helper.layout = self.get_layout(self._helper)

        return self._helper