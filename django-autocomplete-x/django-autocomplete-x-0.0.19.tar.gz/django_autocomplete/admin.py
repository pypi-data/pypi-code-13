from django.contrib import admin

class PublisherStateFilter(admin.FieldListFilter):
    parameter_name = 'status'
    template = 'django_autocomplete/django_autocomplete.html'
    service_url = "/complete/"


    @classmethod
    def make(cls, main_field):
        class Extend(PublisherStateFilter):
            pass
        # end class
        Extend.main_field = main_field
        return Extend
    # end def

    def expected_parameters(self):
        return self.parameter_name
    # end def

    def queryset(self, request, queryset):
    	self.request = request
        pass
    # en ddef

    def choices(self, changelist):
        model = self.field.related_model
        value = self.request.GET.get(self.field_path, '')

        return [{
        	'name': self.field_path,
        	'path': self.request.path,
        	'value': value,
        	'title': self.title.title(),
        	'module': model.__module__,
			'model': model.__name__,
			'url': self.service_url,
			'main_field': self.main_field
        }]
    # end def
# end class