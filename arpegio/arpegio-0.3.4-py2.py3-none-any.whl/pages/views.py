"""Views for the pages app."""
from django.views.generic.detail import DetailView

from .models import Page


class PageDetail(DetailView):
    """Page detail view."""
    model = Page

    def get_template_names(self):
        names = super(PageDetail, self).get_template_names()
        names.append('arpegio-pages/page_detail.html')
        return names
