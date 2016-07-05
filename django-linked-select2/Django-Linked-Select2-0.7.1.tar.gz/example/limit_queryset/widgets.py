from django_select2.forms import ModelSelect2Widget
from linked_select2.forms import LinkedModelSelect2Widget

from .models import Hotel, Room


class HotelSelect2Mixin(object):
    """
    Hotel selecting widget, just like it would have been in django_select2.
    """
    model = Hotel
    search_fields = [
        'name__icontains',
    ]


class HotelSelect2(HotelSelect2Mixin, ModelSelect2Widget):
    pass


class RoomSelect2Mixin(object):
    """
    Narrows down room choices to currently selected hotel.
    """
    model = Room
    search_fields = [
        'name__icontains',
    ]

    def get_queryset(self, form):
        """
        If a linked field contains a hotel, narrow down room choices to that
        particular hotel. Otherwise, return empty list.
        """
        hotel = form.cleaned_data.get('hotel')

        queryset = super().get_queryset()
        if hotel:
            queryset = queryset.filter(hotel=hotel)
        else:
            queryset = queryset.none()

        return queryset


class RoomSelect2(RoomSelect2Mixin, LinkedModelSelect2Widget):
    pass
