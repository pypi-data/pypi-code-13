from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import (
    login,
    logout_then_login,
    password_reset,
    password_reset_complete,
    password_reset_confirm,
    password_reset_done
)
from orgapp.views import (
    index_view,
    dashboard_view,
    about_view,
    #messages,
    organizations,
    profile
)

urlpatterns = [
    url('^$', index_view, name='index'),
    url(r'^dashboard/$', dashboard_view, name='dashboard'),
    url(r'^about/$', about_view, name='about'),
]

# organizations
urlpatterns += [
    url(r'^organizations/filter/(?P<pk>\w+)/$', organizations.organization_detail_view, name='organization_profile'),
    url(r'^organizations/(?P<pk>\w+)/settings/$', organizations.organization_settings_view, name='organization_settings'),
    url(r'^organizations/(?P<pk>\w+)/contact/$', organizations.organization_contact_view, name='contact_organization'),
    url(r'^organizations/filter/$', organizations.organization_list_view, name="list_organization"),
    url(r'^organizations/create/$', organizations.organization_add_view, name='create_organization'),
]

'''
#accounts
urlpatterns += [
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(
        r'^accounts/password/reset/$',
        password_reset,
        {
            'template_name': 'registration/password_reset_request.html',
            'post_reset_redirect': reverse_lazy('password_reset_done'),
        },
        name='password_reset'
    ),
    url(
        r'^accounts/password/reset/done/$',
        password_reset_done,
        {'template_name': 'registration/password_reset_submitted.html'},
        name='password_reset_done'
    ),
    url(
        r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'registration/password_reset_confirmation.html'},
        name='password_reset_confirm'
    ),
    url(
        r'^accounts/password/reset/complete/$',
        password_reset_complete,
        {'template_name': 'registration/password_reset_completed.html'},
        name='password_reset_complete'
    ),
    url(r'^accounts/profile/(?P<pk>\w+)/$', profile.account_profile, name='account_profile'),
    url(r'^accounts/settings/(?P<pk>\w+)/$', profile.EditAccountProfileView, name='account_settings'),
]
'''
