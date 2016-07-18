from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

class AutocompleteWidget(forms.Widget):
	list_display = []
	search_fields = []
	format_data = ''
	service_url = "/complete/"
	model = None

	def __init__(self, model, list_display, search_fields, format_data):
		super(AutocompleteWidget, self).__init__()
		self.model = model
		self.list_display = list_display
		self.search_fields = search_fields
		self.format_data = format_data
    # end def

	def render(self, name, value, attrs={}):
		list_display = ""
		search_fields = ""
		for display in self.list_display:
			list_display = "%s&%s=%s" % (list_display, "list_display", display)
		# end for
		for fields in self.search_fields:
			search_fields = "%s&%s=%s" % (search_fields, "search_fields", fields)
		# end for
		html = """
			<input type="text" id="%(name)s" style="float:left">
			<input id="id_%(name)s" type="hidden" name="%(name)s" value="%(value)s">
			<script type="text/javascript">
				var url = "%(url)s";
				function load_data(value){
					django.jQuery.ajax({
						'url': "%(url_val)s&query="+value,
						success: function(data){
							if (data.suggestions[0]){
								django.jQuery('#%(name)s').val(data.suggestions[0].value);
							}
						}
					});
				}
				load_data("%(value)s");
				django.jQuery("#id_%(name)s").change(function (data){
					load_data(this.value);
				});
				django.jQuery("#%(name)s").autocomplete({
					serviceUrl: url,
					onSelect: function (suggestion) {
						django.jQuery('[name="%(name)s"]').val(suggestion.date);
					}
				});
			</script>
		""" % {
			'name': name,
			'value':value,
			'url': "%s?module_path=%s&model_name=%s&%s&%s&format_data=%s" % (
				self.service_url,
				self.model.__module__,
				self.model.__name__,
				list_display,
				search_fields, 
				self.format_data
			),
			'url_val': "%s?module_path=%s&model_name=%s&%s&%s&format_data=%s" % (
				self.service_url,
				self.model.__module__,
				self.model.__name__,
				list_display,
				"&search_fields=pk", 
				self.format_data
			)
		}
		return mark_safe(html)
	# end def

	class Media:
		css = {
			'all': ('django_autocomplete/css/jquery.autocomplete.css', )
		}
		js = ('django_autocomplete/js/jquery.autocomplete.js', 'admin/js/admin/RelatedObjectLookups.js')
	# end class
# end class

