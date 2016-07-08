from django.forms import ModelForm
from orgapp.models import Organization

class CreateOrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'phone', 'email', 'address', 'max_volunteers', 'min_volunteers']
