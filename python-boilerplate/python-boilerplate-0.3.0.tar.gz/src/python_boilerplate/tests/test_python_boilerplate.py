import os
import tempfile

import mock
import pytest

from python_boilerplate import config as config_mod
from python_boilerplate.config import get_config, get_context
from python_boilerplate.commands import InitProjectConfig, InitProjectWriter


@pytest.yield_fixture
def tempdir():
    tempdir = tempfile.TemporaryDirectory()
    oldpath = os.getcwd()
    with tempdir as path:
        os.chdir(path)
        try:
            yield path
        finally:
            os.chdir(oldpath)
        tempdir.cleanup()


@pytest.yield_fixture
def config(tempdir):
    yield get_config()
    config_mod.GLOBAL_CONFIG = None


@pytest.fixture
def context(config):
    return get_context()


@pytest.fixture
def init_config(config):
    return InitProjectConfig(
        project='test-project',
        pyname='test_project',
        author='some author',
        email='foo@bar.com',
        version='0.1.0',
        license='gpl',
    )


#
# Context
#
def test_default_config_context(context):
    assert context == {
        'project': '',
        'pyname': '',
        'pyname_dashed': '',
        'author': '',
        'email': '',
        'version': '',
        'license': '',
    }


def test_modified_context(config):
    config.set('options', 'project', 'foo-bar')
    config.set('options', 'pyname', 'foo_bar')
    ctx = config_mod.get_context(ham='spam')
    assert ctx['ham'] == 'spam'
    assert ctx['project'] == 'foo-bar'
    assert ctx['pyname'] == 'foo_bar'


def test_init_command_context(config):
    inputs = [
        'test-project',  # project name
        'some author',   # author
        'foo@bar.com',   # email
        '',              # pyname
        '',              # version
        '',              # license
        '',              # editor
    ]
    with mock.patch('builtins.input', side_effect=inputs):
        cfg = InitProjectConfig()
        cfg.run()
        ctx = get_context()

    assert ctx == {
        'project': 'test-project',
        'author': 'some author',
        'email': 'foo@bar.com',
        'pyname': 'test_project',
        'pyname_dashed': 'test-project',
        'version': '0.1.0',
        'license': 'gpl',
    }


#
# File creation
#
def test_create_files(init_config):
    writer = InitProjectWriter(init_config)
    writer.run()
