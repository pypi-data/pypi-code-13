from django.contrib import admin
from .models import Contact
from django.utils.text import Truncator

class ContactAdmin(admin.ModelAdmin):
    list_display = ('sender', 'email', 'created', 'preview')
    fields = ('sender', 'email', 'message', 'created')
    readonly_fields = ('sender', 'email', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('sender', 'email')
    ordering = ('-created',)

    def preview(self, obj):
        return Truncator(obj.message).words(20)

admin.site.register(Contact, ContactAdmin)