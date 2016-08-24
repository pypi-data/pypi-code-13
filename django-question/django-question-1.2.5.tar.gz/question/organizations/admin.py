from django.contrib import admin

from ..nyssance.django.contrib.admin import SuperAdmin

from .models import Organization, Branch, PaymentAccount


class OrganizationAdmin(SuperAdmin):
    list_display = ('id', 'host', 'name')
    search_fields = ('name',)


class BranchAdmin(SuperAdmin):
    list_display = ('id', 'phone_number', 'name')


class PaymentAccountAdmin(SuperAdmin):
    list_display = ('id', 'account_name')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)
