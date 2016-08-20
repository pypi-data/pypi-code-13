import json


class UsergridResponse:

    def __init__(self, json_string):
        self.response = json.loads(json_string)
        self.entity_array = self.response.get('entities', [])

    def first(self):
        if len(self.entity_array) > 0:
            return self.entity_array[0]
        else:
            return None