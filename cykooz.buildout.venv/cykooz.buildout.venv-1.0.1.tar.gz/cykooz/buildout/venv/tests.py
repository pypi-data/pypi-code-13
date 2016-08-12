# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 11.08.2016
"""
from __future__ import unicode_literals, print_function
import os
from collections import namedtuple

import pytest
import zc.buildout.testing


BUILDOUT_CFG = '''
[buildout]
extensions = cykooz.buildout.venv
parts =
'''


@pytest.yield_fixture
def buildout_env():
    TestEnv = namedtuple('TestEnv', ['globs'])
    test_env = TestEnv(globs={})
    zc.buildout.testing.buildoutSetUp(test_env)
    zc.buildout.testing.install_develop('cykooz.buildout.venv', test_env)
    try:
        yield test_env.globs
    finally:
        zc.buildout.testing.buildoutTearDown(test_env)


def test_extension(buildout_env):
    sample_buildout = buildout_env['sample_buildout']
    write = buildout_env['write']
    system = buildout_env['system']
    buildout = buildout_env['buildout']

    write(sample_buildout, 'buildout.cfg', BUILDOUT_CFG)
    res = system(buildout)
    assert 'Install virtual python environment...' in res
    assert 'Virtual python environment was installed.' in res
    assert 'Recreating buildout script.' in res
    assert 'Restarting buildout under virtual python environment.' in res

    parts_dir = os.path.join(sample_buildout, 'parts')
    names = sorted(os.listdir(parts_dir))
    assert names == ['venv']

    venv_bin_path = os.path.join(parts_dir, 'venv', 'bin')
    names = os.listdir(venv_bin_path)
    assert any(name.startswith('python') for name in names)

    with open(buildout, 'rt') as f:
        text = f.read()
    assert venv_bin_path in text

    res = system(buildout)
    assert 'Install virtual python environment...' not in res
    assert 'Virtual python environment was installed.' not in res
    assert 'Recreating buildout script.' not in res
    assert 'Restarting buildout under virtual python environment.' not in res
