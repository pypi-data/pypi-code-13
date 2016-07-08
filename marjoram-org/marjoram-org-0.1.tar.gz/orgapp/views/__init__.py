from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orgapp import models

class IndexView(TemplateView):
    template_name = 'org/index.html'


    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        #context['organizations'] = models.Organization.objects.filter(
        #    creator=self.request.user,
        #)


class DashboardView(ListView):
    template_name = 'org/dashboard.html'
    paginate_by = 10
    model = models.Organization

    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        context['organizations'] = models.Organization.objects.filter(
            creator=self.request.user,
        )

class AboutView(ListView):
    template_name = 'org/about.html'


class NameSearchMixin(object):

	def get_queryset(self):
		queryset = super(NameSearchMixin, self).get_queryset()

		q = self.request.GET.get("q")
		if q:
			return queryset.filter(name__icontains=q)

		return queryset


index_view = IndexView.as_view()
dashboard_view = DashboardView.as_view()
about_view = AboutView.as_view()
