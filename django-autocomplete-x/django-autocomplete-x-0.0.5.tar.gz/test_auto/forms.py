from django import forms
import models
from django_autocomplete import widgets

class MyModelForm(forms.ModelForm):
	def __init__2(self, *args, **kwargs):
		super(MyModelForm, self).__init__(*args, **kwargs)
		widget = self.fields['ref'].widget
		self.fields['ref'].widget.widget = widgets.AutocompleteWidget(
			model=models.MyModel2, 
			list_display=['name', 'pk'], 
			search_fields=['name'], 
			format_data='%(name)s'
		)
	# end class
	class Meta:
		model = models.MyModel
		exclude = ()
	# end class
# end class