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



class OrganizationFilterForm(forms.Form):

    ORGANIZATION_TYPE_CHOICES = (
        ('', '----------'),
    ) + models.Organization.ORGANIZATION_TYPE_CHOICES

    org_type = forms.ChoiceField(
        required=False,
        choices=ORGANIZATION_TYPE_CHOICES,
    )
    pk = forms.IntegerField(
        label='',
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        super(OrganizationFilterForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.iteritems():
            self.fields[key].widget.attrs['class'] = 'form-control'

    def get_organizations(self, initial_qs=None):
        ''' retrieve organizations matching the criteria'''
        if self.errors:
            return models.Organization.objects.none()

        qs = models.Organization.objects.all() if not initial_qs else initial_qs
        data = self.cleaned_data
        if data.get('pk'):
            qs = qs.filter(pk=data['pk'])

        return qs.distinct()

class StateOrganizationForm(forms.Form):
    """Set volunteering as open/close and
    display the min and max volunteers
    """
    pass
