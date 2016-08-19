from django.conf.urls import url
from ..ideia_summernote.views import Upload
urlpatterns = [
    url(r'^upload', Upload.as_view(), name='upload'),

]