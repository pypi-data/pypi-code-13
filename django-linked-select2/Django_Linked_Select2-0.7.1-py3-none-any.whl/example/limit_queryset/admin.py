from django.contrib import admin

from .forms import GuestAdminForm
from .models import Guest


class GuestAdmin(admin.ModelAdmin):
    form = GuestAdminForm


admin.site.register(Guest, GuestAdmin)
