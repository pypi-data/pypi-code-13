# -*- coding: utf-8 -*-

import attr
import os
import six
import yaml


@attr.s
class MigrationTarget(object):
    """Describes a destination for a migrated wiki page."""

    space_key = attr.ib(validator=attr.validators.instance_of(six.string_types))
    title = attr.ib(validator=attr.validators.instance_of(six.string_types))
    parent_title = attr.ib(default='', validator=attr.validators.instance_of(six.string_types))


@attr.s
class MigrationStep(object):
    """Describes a single step for a GitHub-to-Confluence migration."""

    migration_target = attr.ib(validator=attr.validators.instance_of(MigrationTarget))
    filename = attr.ib(validator=attr.validators.instance_of(six.string_types))


@attr.s
class Project(object):
    """Describes a GitHub-to-Confluence migration project."""

    migration_steps = attr.ib(default=attr.Factory(list))


def title_from_filename(filename):
    basename = os.path.splitext(os.path.basename(filename))[0]
    return basename.replace('-', ' ')


def project_from_config(data):
    project = Project()
    default_migration_target_attrs = data.get('target', {})
    for step_attrs in data.get('steps', []):
        migration_target_attrs = dict(default_migration_target_attrs)
        migration_target_attrs.update(step_attrs.get('target', {}))
        migration_target_attrs.setdefault('title', title_from_filename(step_attrs['filename']))
        migration_target = MigrationTarget(**migration_target_attrs)
        migration_step = MigrationStep(migration_target, step_attrs['filename'])
        project.migration_steps.append(migration_step)
    return project


def project_from_config_file(filename):
    with open(filename) as config_file:
        config = yaml.load(config_file)
        return project_from_config(config['project'])
