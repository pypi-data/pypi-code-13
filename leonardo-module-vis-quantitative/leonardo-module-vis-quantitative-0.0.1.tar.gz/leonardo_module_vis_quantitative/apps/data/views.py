
import json
import math
import traceback
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import View
from feincms.views.decorators import standalone
from leonardo.module.web.widgets.utils import get_widget_from_id


class WidgetDataView(View):

    '''This view call specific method on widget end returns JSON

    requires ``widget_id`` and optionaly ``method=get_all_data``
    which is name of method on the widget
    ``kwargs`` are propagated down to widget method

    Do not serialize data in widget methods
    '''

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @cached_property
    def attrs(self):
        return self.request.POST

    @method_decorator(standalone)
    def post(self, *args, **kwargs):

        # if self.request.is_ajax():
        try:
            id = self.attrs['widget_id']
        except KeyError:
            return JsonResponse({'error':
                                 'Widget_id param not found in %s.' % self.attrs})

        widget = get_widget_from_id(id)

        if not widget:
            return JsonResponse({'error': 'Widget "%s" not found' % id})

        if 'method' not in self.attrs:
            method_name = 'get_data'
        else:
            method_name = self.attrs['method']

        method = getattr(widget, method_name, None)

        if not method or not callable(method):
            return JsonResponse({'error':
                                 'The method %s is not callable'
                                 ' on %s'
                                 % (method_name, id)})

        try:

            kw = json.loads(self.attrs.get('kwargs', "{}"))

            if method_name == 'get_update_data':
                kw['expected_timestamp'] = math.floor(float(self.attrs.get('expected_timestamp', '0')))

            cache_key = '.'.join([
                widget.cache_data_key,
                method_name,
            ] + ['%s-%s' % (v[0], v[1]) for v in kw.items()])

            data = widget.cache.get(cache_key)

            if data is None:

                kw.update({'request': self.request})
                data = method(**kw)

                widget.cache.set(cache_key,
                                 data, getattr(widget, 'refresh_interval', 60))

        except Exception as e:

            response = {'error': str(e)}

            if settings.DEBUG:
                response['traceback'] = traceback.format_exc()

            return JsonResponse(response)

        else:
            return JsonResponse({'data': data, 'id': id})

        return HttpResponseForbidden()
