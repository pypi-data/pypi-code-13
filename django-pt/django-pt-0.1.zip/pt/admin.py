from django.contrib import admin
import pt.models

# Register your models here.

admin.site.register(pt.models.Project)
admin.site.register(pt.models.ProjectNumbers)
admin.site.register(pt.models.PINumbers)
admin.site.register(pt.models.Nepa)
admin.site.register(pt.models.Air)
admin.site.register(pt.models.Noise)
admin.site.register(pt.models.Ecology)
admin.site.register(pt.models.Aquatics)
admin.site.register(pt.models.Archaeology)
admin.site.register(pt.models.History)