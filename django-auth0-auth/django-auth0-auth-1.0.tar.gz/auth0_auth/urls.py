from .views import auth, callback
from django.conf.urls import url


urlpatterns = [
    url(r'^login/$', auth, name='auth0_login'),
    url(r'^callback/$', callback, name='auth0_callback'),
]
