import json
import dateutil.parser
from forest.services.utils import merge_dicts, get_model_class
from forest.generators import schemas


class ResourceCreator():
    def __init__(self, request, model_name):
        self.body = json.loads(request.body)
        self.model_name = model_name
        self.model = get_model_class(model_name)

    def perform(self):
        kw_params_list = []
        for field, value in self.body['data'].get('attributes', {}).iteritems():
            if value:
                field_type = schemas.api_map.get_type(self.model_name, field)
                if field_type == 'Date':
                    value = dateutil.parser.parse(value)
                elif field_type == 'Number':
                    value = float(value)
                kw_params_list.append({'%s' % field: value})


        for k, v in self.body['data'].get('relationships', {}).iteritems():
            if not isinstance(v['data'], list):
                kw_params_list.append({"%s_id" % k: v['data'].get('id')})

        kw_params = merge_dicts(*kw_params_list)
        item = self.model(**kw_params)
        item.save()
        return item

