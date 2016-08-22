# -*- encoding: utf-8
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class SoundFile(models.Model):
    TYPE_CHOICES = (
        ('wav', 'wav'),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.FileField(upload_to=settings.OUTPUT_DIR)
    text = models.TextField(blank=False)
    command = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    dc = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True)
    def __str__(self):
        return '%s' % self.uuid