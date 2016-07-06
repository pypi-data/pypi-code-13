from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import UserSession


admin.site.register(UserSession)
admin.site.register(Session)
