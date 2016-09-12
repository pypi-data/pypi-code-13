from django.contrib import admin
from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_actived', 'created', 'updated')
    list_per_page = 12
    list_filter = ['is_actived', 'created', 'updated']
    search_fields = ['name']

admin.site.register(City, CityAdmin)
