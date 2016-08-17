# -*- coding: utf-8 -*-
import autocomplete_light

from django.http import Http404


class PermissionAutocompleteModelBase(autocomplete_light.AutocompleteModelBase):

    def has_permission(self, request):
        return True

    def choices_for_request(self):

        if not self.has_permission(self.request):
            raise Http404
        return super(PermissionAutocompleteModelBase, self).choices_for_request()


class SuperUserAutocompleteModelBase(PermissionAutocompleteModelBase):

    def has_permission(self, request):
        return request.user.is_superuser
