from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_openpay_repo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^openpay/', include('django_openpay.urls')),
    url(r'^testing/$', TemplateView.as_view(template_name='testing.jinja'),
        name='home'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
