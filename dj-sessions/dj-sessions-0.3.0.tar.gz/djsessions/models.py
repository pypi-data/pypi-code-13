# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models

from model_utils.models import TimeStampedModel


class UserSession(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    # session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    session_key = models.CharField('session key', max_length=40, unique=True)

    def __str__(self):
        return self.user.username
