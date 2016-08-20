# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.UserProfile)
class UserInfoAdmin(admin.ModelAdmin):
    """
    用户帐户管理
    """
    search_fields = ['domain', 'uid', 'nickname']
    readonly_fields = ['time_updated']


@admin.register(models.UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    """
    用户注册验证管理
    """
    search_fields = ['uid', 'fullname']
    readonly_fields = ['time_updated']
