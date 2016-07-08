from django import forms
from django.forms.formsets import formset_factory
from django.forms.extras import widgets
from django.contrib.admin import widgets as admin_widgets
from django.core.exceptions import ValidationError
from orgapp import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group, Permission


class ContactForm(forms.Form):
    username = forms.EmailField(label=_("Email"),
                            max_length=75,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.ChoiceField(
        required=True,
        choices=(
            ('question', 'Question'),
            ('problem', 'Problem'),
            ('suggestion', "Suggestion"),
            ('other', 'Other Issue')
        )
    )
    message = forms.CharField(
        required=False, label=_("Message"), max_length=1000, min_length=5,
        widget=forms.widgets.Textarea(attrs={'class': 'form-control'})
    )
