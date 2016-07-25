from datetime import datetime
from django.utils import timezone
from django.db import models


class PatchLog(models.Model):
    patch = models.CharField(max_length=255, unique=True)
    added = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = u'patch_log'
