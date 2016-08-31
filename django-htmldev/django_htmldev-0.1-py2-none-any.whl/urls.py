from django.conf.urls import url
from . import views


urlpatterns = [
    url('^(?P<path>.*)/', views.HtmlDev.as_view()),
]
