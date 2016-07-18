from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
import importlib
import datetime
import json

def complete(request):
	module_path = request.GET.get('module_path', False) 
	model_name = request.GET.get('model_name', False) 
	search_fields = request.GET.getlist('search_fields') 
	list_display = request.GET.getlist('list_display')
	format_data = request.GET.get('format_data', False)
	paginated_by = request.GET.get('paginated_by', '10')
	date_format = "%d/%m/%Y"
	datetime_format = "%d/%m/%Y %I:%M%p"
	query = request.GET.get('query', '') 

	if module_path and model_name and paginated_by.isdigit():
		module = importlib.import_module(module_path)
		if hasattr(module, model_name):
			model = getattr(module, model_name)
			queryset = model.objects.all()
			q = False
			for column in search_fields:
				if column != 'pk':
					kwargs = {
						'{0}__{1}'.format(column, 'icontains'): query, 
					}
				else:
					kwargs = {
						'pk': query
					}
				# end if
				if q:
					q = q | Q(**kwargs)
				else:
					q = Q(**kwargs)
				# end if
			#end for
			if q:
				queryset = queryset.filter(q)
			# end if
			rows = []
			for obj in queryset[0:int(paginated_by)]:
				row = {}
				for field in list_display:
					val = getattr(obj, field)
					if isinstance(val, datetime.datetime):
						row[field] = val.strftime(datetime_format)
					elif isinstance(val, datetime.date):
						row[field] = val.strftime(date_format)
					else:
						row[field] = unicode(val)
					# end if
				# end for
				if format_data == '':
					format_data = str(obj)
				# end if

				rows.append({
					'date': str(obj.pk),
					'value': format_data % row
				})
			# end for
			response = {
				"query": query,
				"suggestions": rows
			}
			return HttpResponse(json.dumps(response), content_type="application/json")
		# end if
	# end if
	return HttpResponse("[]")
# end def