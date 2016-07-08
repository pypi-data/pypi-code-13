from django.conf import settings
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView, FormView, RedirectView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormView
from django import forms
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate, REDIRECT_FIELD_NAME
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView

from orgapp.models import UserProfile
from orgapp.forms import UserForm

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


@method_decorator(login_required)
def EditAccountProfileView(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('phone', 'address', 'address2', 'city', 'state', 'zipcode'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset
        })
    else:
        raise PermissionDenied
   

class AccountProfileView(DetailView):
    template_name = 'org/user_profile.html'
    model = User


'''
Superusers profile page, edit avatar password etc
'''

class AdminUpdateView(UpdateView):
    pass


class AdminProfileView(DetailView):
    pass


account_profile = AccountProfileView.as_view()


admin_profile = AdminProfileView.as_view()
admin_settings = AdminUpdateView.as_view()
