from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


class IndexView(TemplateView):
    template_name = 'maccman/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class LoginView(FormView):
    template_name = 'maccman/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('maccman:index')


def logout_view(request):
    logout(request)
    return redirect('maccman:index')
