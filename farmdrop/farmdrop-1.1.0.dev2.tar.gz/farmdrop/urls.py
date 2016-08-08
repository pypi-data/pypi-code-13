from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

from saleor.cart.urls import urlpatterns as cart_urls
from saleor.checkout.urls import urlpatterns as checkout_urls
from saleor.core.sitemaps import sitemaps
from saleor.core.urls import urlpatterns as core_urls
from saleor.order.urls import urlpatterns as order_urls
from saleor.product.urls import urlpatterns as product_urls
from saleor.registration.urls import urlpatterns as registration_urls
from saleor.userprofile.urls import urlpatterns as userprofile_urls
from saleor.dashboard.urls import urlpatterns as dashboard_urls


admin.autodiscover()

urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^account/', include(registration_urls, namespace='registration')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/', include(cart_urls, namespace='cart')),
    url(r'^checkout/', include(checkout_urls, namespace='checkout')),
    url(r'^dashboard/', include(dashboard_urls, namespace='dashboard')),
    url(r'^order/', include(order_urls, namespace='order')),
    url(r'^products/', include(product_urls, namespace='product')),
    url(r'^profile/', include(userprofile_urls, namespace='profile')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'', include('payments.urls')),
    url(r'^robots.txt', include('robots.urls')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    import debug_toolbar
    from django.views.static import  serve
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^__debug__/', include(debug_toolbar.urls))
        ]
