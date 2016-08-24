from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..nyssance.django.contrib.admin import SuperAdmin

from .models import Card


class CardAdminForm(forms.ModelForm):
    tags = forms.CharField(label=_('tags'), widget=forms.Textarea, required=False)

    class Meta:
        model = Card
        fields = '__all__'


class CardAdmin(SuperAdmin):
    list_display = ('id', 'caption', 'url', 'get_preview', 'repost_count', 'created_time', 'is_active')
    list_filter = ('user_id', 'type')
    search_fields = ('user_id', 'type')
    form = CardAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.object_id = 1  # 测试的时候打开.
        super(CardAdmin, self).save_model(request, obj, form, change)


admin.site.register(Card, CardAdmin)
