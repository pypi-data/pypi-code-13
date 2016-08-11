# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from .convert import markdown_to_confluence
from .confluence import client_from_config_file
from .project import project_from_config_file


DRY_RUN = os.environ.get('DRY_RUN', '').lower() in ('y', 'yes', 'true', 'on', '1')
DEBUG_MODE = os.environ.get('DEBUG', '').lower() in ('y', 'yes', 'true', 'on', '1')


def debug(*args, **kwargs):
    kwargs['file'] = sys.stderr
    if DEBUG_MODE:
        print(*args, **kwargs)


def copy_content(content, confluence, target):
    parent_page_id = None

    if target.parent_title:
        parent_page_id = confluence.get_page_by_title(target.space_key, target.parent_title)['id']

    existing_page = confluence.get_page_by_title(target.space_key, target.title)
    body = markdown_to_confluence(content)

    if DRY_RUN:
        print(body, file=sys.stderr)
        return

    if existing_page:
        confluence.update_page(existing_page, body)
    else:
        confluence.create_page(space_key=target.space_key,
                               title=target.title,
                               body=body,
                               parent_page_id=parent_page_id)


def main():
    config_location = os.getcwd()
    config_filename = os.path.join(config_location, '.gh2conf.yaml')
    project = project_from_config_file(config_filename)

    config_overrides = {}
    if 'CONFLUENCE_PASSWORD' in os.environ:
        config_overrides['password'] = os.environ['CONFLUENCE_PASSWORD']

    confluence = client_from_config_file(config_filename, config_overrides)

    for step in project.migration_steps:
        debug('Copying', step.filename, 'to', step.migration_target.space_key, '-> ', end='')
        if step.migration_target.parent_title:
            debug(step.migration_target.parent_title, '-> ', end='')
        debug(step.migration_target.title)
        with open(step.filename, 'rb') as source_file:
            content = source_file.read().decode('utf-8')
        copy_content(content, confluence, step.migration_target)


main()
