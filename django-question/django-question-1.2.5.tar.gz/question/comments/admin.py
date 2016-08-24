from django.contrib import admin

from ..nyssance.django.contrib.admin import SuperAdmin

from .models import Comment


class CommentAdmin(SuperAdmin):
    list_display = ('id', 'user_id', 'card_id', 'text', 'created_time')
    list_filter = ('user_id', 'card_id')
    search_fields = ('user_id', 'card_id')

admin.site.register(Comment, CommentAdmin)
