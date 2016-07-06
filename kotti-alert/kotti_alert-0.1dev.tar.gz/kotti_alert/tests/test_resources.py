# -*- coding: utf-8 -*-

"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pytest import raises


def test_model(root, db_session):
    from kotti_alert.resources import CustomContent

    cc = CustomContent()
    assert cc.custom_attribute is None

    cc = CustomContent(custom_attribute=u'Foo')
    assert cc.custom_attribute == u'Foo'

    root['cc'] = cc = CustomContent()
    assert cc.name == 'cc'

    with raises(TypeError):
        cc = CustomContent(doesnotexist=u'Foo')
