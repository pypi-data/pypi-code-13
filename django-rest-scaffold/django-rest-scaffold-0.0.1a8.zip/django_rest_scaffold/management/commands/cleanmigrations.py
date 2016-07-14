# -*- coding: UTF-8 -*-
"""
    Created by Régis Eduardo Crestani <regis.crestani@gmail.com> on 19/06/2016.
"""
import os
from django.core.management.base import BaseCommand
from django_rest_scaffold.settings import DJANGO_REST_SCAFFOLD_SETTINGS as SETTINGS


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Searching files to remove...')
        for root, dir_names, file_names in os.walk(SETTINGS['APPS_FOLDER']):
            if root.endswith('migrations'):
                for file_name in file_names:
                    if file_name != '__init__.py':
                        file_path = os.path.join(root, file_name)
                        os.remove(file_path)
                        print('    deleted %s' % file_path)
