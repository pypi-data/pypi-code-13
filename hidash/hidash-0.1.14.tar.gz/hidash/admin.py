from django.contrib import admin
import models


class ChartMetricInlineAdmin(admin.TabularInline):
    model = models.ChartMetric
    fk_name = 'chart'
    extra = 1


class ChartAuthPermissionInlineAdmin(admin.TabularInline):
    model = models.ChartAuthPermission
    fk_name = 'chart'
    extra = 1


class ChartAuthGroupInlineAdmin(admin.TabularInline):
    model = models.ChartAuthGroup
    fk_name = 'chart'
    extra = 1


class ChartGroupInlineAdmin(admin.TabularInline):
    model = models.ChartGroup
    fk_name = 'chart'
    extra = 1


class ChartAdmin(admin.ModelAdmin):
    inlines = [
        ChartMetricInlineAdmin, ChartAuthPermissionInlineAdmin,
        ChartAuthGroupInlineAdmin, ChartGroupInlineAdmin
    ]


admin.site.register(models.Chart, ChartAdmin)
