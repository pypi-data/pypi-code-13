from django.contrib import admin
from django.db import models
from django.db.models import TextField

from . import models as app_models


for name in dir(app_models):
    model_class = getattr(app_models, name)
    if name[0].isupper() and issubclass(model_class, models.Model):
        print(model_class)

        class A(admin.ModelAdmin):
            search_fields = list_display = [field.attname for field in model_class._meta.fields]

        admin.site.register(model_class, A)

