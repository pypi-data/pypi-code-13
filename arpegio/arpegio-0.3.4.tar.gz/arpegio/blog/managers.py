"""Blog managers."""
from django.db import models
from django.utils.timezone import now


class PostManager(models.Manager):  # pylint: disable=too-few-public-methods
    """Post manager"""

    def public(self):
        """Filter the queryset to obtain the public posts."""
        return self.filter(status='PB', creation_date__lt=now())

    def sticky(self):
        """Filter the queryset to obtain the sticky posts."""
        return self.filter(sticky=True)
