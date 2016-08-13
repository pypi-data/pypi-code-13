from django.contrib import admin
from django.contrib.auth import get_user_model
from notifications.admin import NotificationAdminMixin


User = get_user_model()


class UserAdmin(NotificationAdminMixin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
