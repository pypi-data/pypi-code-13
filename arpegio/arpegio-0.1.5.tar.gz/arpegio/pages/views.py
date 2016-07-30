"""Views for the pages app."""
from django.views.generic.detail import DetailView

from .models import Page


class PageDetail(DetailView):
    """Page detail view."""
    model = Page
