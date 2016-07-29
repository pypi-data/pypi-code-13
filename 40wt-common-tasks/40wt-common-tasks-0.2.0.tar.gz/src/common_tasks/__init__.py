# coding: utf-8

import re
import os
import sys

from invoke import task, run

__version__ = '0.2.0'


@task
def update_requirements(
        ctx,
        path='.',
        pattern=r'^(requirements[^/]*\.in|requirements/.*\.in)$',
        upgrade=True):
    """Compiles requirements.in into requirements.txt using pip-compile
    """
    requirements_files = []

    regex = re.compile(pattern)

    for root, dir, files in os.walk(path):
        for filename in files:
            full_path = os.path.relpath(
                os.path.join(root, filename),
                path)

            if regex.match(full_path) is not None:
                requirements_files.append(full_path)

    for filename in requirements_files:
        command = ['pip-compile']
        if upgrade:
            command.append('--upgrade')
        command.append(filename)
        run(' '.join(command))


def get_current_version():
    """Берет самую последнюю версию из CHANGELOG.md
    Считаем, что она прописана в первой строчке, так:

    ## 0.1.2 (2016-02-13)

    Или без ##.
    """
    with open('CHANGELOG.md') as f:
        first_line = f.readline()
        return first_line.strip('#').split()[0]


def make_dashed_aliases(items):
    """Делает алиасы для invoke тасков, заменяя '_' на '-'.

    Использовать надо так, в конце tasks.py:

    make_dashed_aliases(locals().values())
    """
    for item in items:
        if hasattr(item, 'aliases'):
            item_name = item.__name__
            replaced = item_name.replace('_', '-')
            if replaced != item_name and replaced not in item.aliases:
                item.aliases += (replaced,)


def is_dirty_workdir():
    """Returns True, if there is non pushed commits, or not commited code in the repository.
    """

    result = run('git status --porcelain', hide=True, warn=True)
    if result.return_code != 0:
        # something went wrong
        return True

    if result.stdout:
        # there is not commited files
        return True

    # now check if there are unpushed commits
    result = run('git log @{upstream}..', hide=True, warn=True)
    if result.return_code != 0:
        # probably there isn't upstream
        return True

    if result.stdout:
        # there are non pushed commits
        return True

    return False


@task
def check_if_dirty(ctx):
    yes = is_dirty_workdir()
    if yes:
        print 'Please, commit/ignore all files and push to upstream.'
        sys.exit(1)
