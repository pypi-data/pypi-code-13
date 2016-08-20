# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User

from django_simple_profile.utils.token import random_str
from .. import models


class MyUserProfile(models.UserProfile):
    class Meta:
        proxy = True

    @classmethod
    def get_by_uid(cls, uid):
        """
        根据个性获取用户信息
        :param uid:
        :return:
        """
        return cls.objects.filter(uid=uid).first()

    @classmethod
    def get_by_domain(cls, domain):
        """
        根据个性获取用户信息
        :param domain:
        :return:
        """
        return cls.objects.filter(domain=domain).first()

    @classmethod
    def get_by_nickname(cls, nickname):
        """
        根据nickname获取用户信息
        :param nickname:
        :return:
        """
        return cls.objects.filter(nickname=nickname).first()

    @classmethod
    def create_user(cls, email, password, nickname):
        """
        创建用户资料
        1.新建用户
        2.创建附加信息
        :param password:
        :param email:
        :param nickname:
        :return:
        """
        user = User()
        user.username = email
        user.set_password(password)
        user.email = email
        user.save(force_insert=True)

        info = cls()
        info.uid = user.id
        info.nickname = nickname
        domain = random_str(6)
        rnd_count_max = 10
        rnd_count_i = 0
        while cls.get_domain(domain):
            rnd_count_i += 1
            domain = random_str(6)
            if rnd_count_i > rnd_count_max:
                raise Exception('无法获取唯一随机域名')

        info.domain = domain
        info.save(force_insert=True)
        return info
