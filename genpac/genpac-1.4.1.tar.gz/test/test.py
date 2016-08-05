# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division
import os
import sys
from pprint import pprint
from contextlib import contextmanager

from nose.tools import eq_, assert_list_equal

from genpac import core

_test_path = os.path.dirname(__file__)
_sys_argv = sys.argv

_proxy_cmd = '_PROXY_'
_test_config_file = os.path.join(_test_path, 'config.ini')
_test_user_rule_file = os.path.join(_test_path, 'user_rules.txt')
_test_argv = ['genpac', '-p', _proxy_cmd]

_test_rules = {
    '! COMMENT': None,
    '||azubu.tv': 'azubu.tv',
    '||crossfire.co.kr': 'crossfire.co.kr',
    '||darpa.mil': 'darpa.mil',
    '|http://85.17.73.31/': None,
    '|http://img.dlsite.jp/': 'dlsite.jp',
    '|http://imgmega.com/*.gif.html': 'imgmega.com',
    '@@|http://blog.ontrac.com': 'ontrac.com'
}


@contextmanager
def patch_sys_argv(val_lst):
    old_val = getattr(sys, 'argv')
    new_value = _test_argv
    new_value.extend(val_lst)
    setattr(sys, 'argv', new_value)
    yield
    setattr(sys, 'argv', old_val)


def setup():
    pass


def teardown():
    pass


def test_get_public_suffix():
    eq_(core.get_public_suffix('api.google.com'), 'google.com')


def test_config():
    # 默认参数
    with patch_sys_argv(['--gfwlist-url=']):
        cfg = core.parse_config()
        assert_list_equal(
            [cfg.proxy, cfg.compress, cfg.precise, cfg.gfwlist_url],
            [_proxy_cmd, None, None, core.GFWLIST_URL])

    # 空配置文件，所有选项默认
    with patch_sys_argv(['-c', os.path.join(_test_path, 'config-empty.ini')]):
        cfg = core.parse_config()
        assert_list_equal(
            [cfg.proxy, cfg.compress, cfg.precise, cfg.gfwlist_url],
            [_proxy_cmd, False, False, core.GFWLIST_URL])

    with patch_sys_argv(['-c', _test_config_file, '--precise', '--compress']):
        cfg = core.parse_config()
        assert_list_equal(
            [cfg.proxy, cfg.compress, cfg.precise, cfg.gfwlist_url],
            [_proxy_cmd, True, True, core.GFWLIST_URL])


def test_surmise_domain():
    # pprint(core.parse_rules(_test_rules.keys()))
    # pprint(core.parse_rules_precise(_test_rules.keys()))
    pprint(core.parse_rules(['|http://cthlo.github.io/hktv']))
    # pprint(core.get_public_suffix('http://cthlo.github.io/hktv'))
