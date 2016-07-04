from django.contrib import admin

from models import QuantitativeDataSource, QuantitativeData


class QuantitativeDataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'data']

admin.site.register(QuantitativeDataSource, QuantitativeDataSourceAdmin)


class QuantitativeDataAdmin(admin.ModelAdmin):
    list_display = ['data_source', 'metrics']

admin.site.register(QuantitativeData, QuantitativeDataAdmin)
