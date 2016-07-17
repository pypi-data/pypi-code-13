# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class SimpleEmailMessageForm(forms.Form):
    subject = forms.CharField(max_length = 100, label = _("Subject"))
    sender_email = forms.EmailField(label = _("Sender e-mail"))
    sender_name = forms.CharField(max_length = 100, required = False, label = _("Sender name"))
    recipient_email = forms.EmailField(label = _("Recipient e-mail"))
    recipient_name = forms.CharField(max_length = 100, required = False, label = _("Recipient name"))
    message = forms.CharField(widget = forms.Textarea, label = _("Message"))
    html_mimetype = forms.BooleanField(required = False, label = _("HTML MIME type"))
