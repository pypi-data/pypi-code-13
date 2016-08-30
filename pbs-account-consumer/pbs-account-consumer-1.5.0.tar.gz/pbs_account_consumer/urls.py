from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_begin, name='login_begin'),
    url(r'^login/immediate/$', views.login_begin, {'immediate': True},
        name='login_begin_immediate'),
    url(r'^complete/$', views.login_complete),
    url(r'^setup_needed/$', views.setup_needed, name='login_setup_needed'),
    url(r'^change_password/$', views.change_password),
    url(r"^change_password/complete$", views.ax_change_complete)
]
