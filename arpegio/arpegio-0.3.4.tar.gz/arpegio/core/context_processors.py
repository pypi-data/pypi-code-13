"""Arpegio's context_processors."""
from .settings import site


def settings(request):  # pylint: disable=unused-argument
    """Return the arpegio's settings."""
    return {'arpegio': site.settings}
