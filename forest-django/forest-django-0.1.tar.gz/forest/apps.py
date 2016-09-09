import json
import requests
import os

from django.conf import settings
from django.apps import AppConfig
from forest.generators.schemas import api_map
from forest.services.utils import get_model_class

class ForestConfig(AppConfig):
    name = 'forest'
    verbose_name = "My Forest Connector"
    def ready(self):
        apimap = api_map.generate()
        url = os.getenv('FOREST_URL', getattr(settings, 'FOREST_URL',
             'https://forestadmin-server.herokuapp.com'))
        url += '/forest/apimaps'
        secret_key = os.getenv('FOREST_SECRET_KEY', settings.FOREST_SECRET_KEY)
        headers = {
            'forest-secret-key':  secret_key,
            'Content-Type': 'application/json'
        }
        req = requests.post(url, data=json.dumps(apimap), headers=headers)
