from django.contrib import admin
import models
import forms

class MyModelAdmin(admin.ModelAdmin):
	form = forms.MyModelForm
# end class

admin.site.register(models.MyModel, MyModelAdmin)
admin.site.register(models.MyModel2)
