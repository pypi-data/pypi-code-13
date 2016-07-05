from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Hotel
from .widgets import HotelSelect2, RoomSelect2


class RoomWidgetForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())


class GuestAdminForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        room = cleaned_data.get('room')
        hotel = cleaned_data.get('hotel')

        if room is not None:
            if hotel is None:
                self.add_error(
                    'room',
                    _("Cannot set room without setting hotel.")
                )
            elif room.hotel != hotel:
                self.add_error(
                    'room',
                    _("'%(room)s' is not a room of '%(hotel)s' hotel." % {
                        'room': room,
                        'hotel': hotel,
                    })
                )

    class Meta:
        widgets = {
            'hotel': HotelSelect2,
            'room': RoomSelect2(form=RoomWidgetForm),
        }
