from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from dcl_sites.views import (
    ContentStaffView,
    DirectoryStaffView,
    DomainStaffView,
    PageView,
)


urlpatterns = [
    url(r'^$', PageView.as_view()),
    url(r'^_domain/$', DomainStaffView.as_view()),
    url(r'^_directory(?P<url>.*)$', DirectoryStaffView.as_view()),
    url(r'^_content(?P<url>.*)$', ContentStaffView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^account/social/accounts/$', TemplateView.as_view(template_name='account/social.html'), name='account_social_accounts'),
    url(r'^account/social/', include('social.apps.django_app.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    '',
    url(r'^(?P<url>.*)$', PageView.as_view()),
)
