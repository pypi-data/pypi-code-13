# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib import admin
from django.db import transaction
from django.utils.timezone import now

from .models import Author, Category, Entry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class EntryAdminForm(forms.ModelForm):
    subtitle = forms.CharField(widget=forms.TextInput(attrs={'size': 100}),
                               required=False)
    abstract = forms.CharField(widget=forms.Textarea(attrs={'cols': 100}),
                               required=False)
    date = forms.SplitDateTimeField(widget=AdminSplitDateTime, required=False)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm
    readonly_fields = ('author',)
    prepopulated_fields = {
        'slug': ('title',),
    }

    def has_add_permission(self, request):
        return super(EntryAdmin, self).has_add_permission(request) and \
            Author.is_author(request.user)

    def has_change_permission(self, request, obj=None):
        return super(EntryAdmin, self).has_change_permission(
            request, obj) and Author.is_author(request.user)

    def has_delete_permission(self, request, obj=None):
        return super(EntryAdmin, self).has_delete_permission(
            request, obj) and Author.is_author(request.user)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not change:
            author = Author.objects.get(user=request.user)
            obj.author = author

        if obj.date is None:
            obj.date = now()

        obj.save()

admin.site.register(Author)
