"""Blog managers."""
from django.db import models


class PostManager(models.Manager):  # pylint: disable=too-few-public-methods
    """Post manager"""

    def public(self):
        """Filter the queryset to obtain the public posts."""
        return self.filter(status='PB')
