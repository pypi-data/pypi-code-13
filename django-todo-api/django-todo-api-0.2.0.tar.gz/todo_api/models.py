"""Models for the todo API."""
from django.conf import settings
from django.db import models


class Task(models.Model):
    """A representation of a task."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        """Convert the instance to a string.

        Returns:
            str:
                The instances `title` attribute.
        """
        return self.title
