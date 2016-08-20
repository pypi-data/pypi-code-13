# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from .. import models


class MyUserDetail(models.UserDetail):
    class Meta:
        proxy = True

    @classmethod
    def get_uid(cls, uid):
        """
        根据个性获取用户信息
        :param uid:
        :return:
        """
        return cls.objects.filter(uid=uid).first()
