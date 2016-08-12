"""Views for the tags app."""
from django.views.generic.detail import DetailView

from .models import Tag


class TagDetail(DetailView):
    """Tag detail view."""
    model = Tag

    def get_template_names(self):
        names = super(TagDetail, self).get_template_names()
        names.append('arpegio-tags/tag_detail.html')
        return names
