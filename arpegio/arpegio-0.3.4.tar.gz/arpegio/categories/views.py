"""Views for the categories app."""
from django.views.generic.detail import DetailView

from .models import Category


class CategoryDetail(DetailView):
    """Category detail view."""
    model = Category

    def get_template_names(self):
        names = super(CategoryDetail, self).get_template_names()
        names.append('arpegio-categories/category_detail.html')
        return names
