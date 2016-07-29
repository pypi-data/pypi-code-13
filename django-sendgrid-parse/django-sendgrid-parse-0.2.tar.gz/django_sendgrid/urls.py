from django.conf.urls import include, url

from django.contrib import admin
from django_sendgrid_parse import urls
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_sendgrid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^sendgrid/', include(urls.urlpatterns)),
]
