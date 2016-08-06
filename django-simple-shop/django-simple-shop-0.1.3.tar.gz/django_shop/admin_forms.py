from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from PIL import Image

from .utils import delivery
from .utils.payment import get_model_choices


class ProductImageAdminForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data['image']
        im = Image.open(image)
        width, height = im.size
        if width < 600:
            raise ValidationError(
                _('Image is to small: width (%(width)s) is lower than 600'),
                code='invalid',
                params={'width': width},
            )
        return image


class PaymentTypeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentTypeAdminForm, self).__init__(*args, **kwargs)
        self.fields['payment_hook'].widget = forms.Select(
            choices=get_model_choices())


class DeliveryTypeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryTypeAdminForm, self).__init__(*args, **kwargs)
        self.fields['delivery_hook'].widget = forms.Select(
            choices=delivery.get_model_choices())

    def clean(self):
        data = self.cleaned_data
        if 'pricing_method' not in data:
            return data

        if data['pricing_method'] in (delivery.METHOD_PERCENT,
                                      delivery.METHOD_CONSTANT):
            if not data.get('price'):
                raise ValidationError(
                    _('You need to enter price')
                )
        elif data['pricing_method'] == delivery.METHOD_API:
            if data.get('price'):
                raise ValidationError(
                    _('You should not enter price')
                )
            if not data.get('pricing_hook') == '-':
                raise ValidationError(
                    _('You should provide pricing_hook')
                )
        elif data['pricing_method'] == delivery.METHOD_FREE:
            if data.get('price'):
                raise ValidationError(
                    _('You should not enter price')
                )
        return data
