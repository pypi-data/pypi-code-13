# -*- coding: UTF-8 -*-
"""
用户帐号模块
"""

from __future__ import unicode_literals

from django.core import validators
from django.db import models
from django.utils.timezone import now


class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = '用户信息'
        verbose_name = '用户信息'

    uid = models.IntegerField('用户ID', primary_key=True)

    nickname = models.CharField('笔名', max_length=30, db_index=True, unique=True,
                                help_text='请填写您的笔名，该笔名将作为您的公开称呼，且不能与他人相同',
                                validators=[
                                    validators.RegexValidator(
                                        r'^.{3,20}$',
                                        '请使用3-30个中英文数字等组合'
                                    ),
                                ],
                                error_messages={
                                    'unique': "该笔名已存在，请更换",
                                }, )

    domain = models.CharField('个性域名', max_length=30, db_index=True, unique=True,
                              help_text='请使用3-20个字符的字母、数字、-、_组合，且不能与他人相同',
                              validators=[
                                  validators.RegexValidator(
                                      r'^[\w\d\-_]{3,20}$',
                                      '请使用3-20个字符的字母、数字、-、_组合'
                                  ),
                              ],
                              error_messages={
                                  'unique': "该个性域名已存在，请更换",
                              }, )
    time_updated = models.DateTimeField('更新时间', default=now)
    avatar = models.ImageField('头像', max_length=255, blank=True, null=True)
    point = models.IntegerField('积分', default=0)
    message_num = models.IntegerField('消息', default=0)
    settings = models.CharField("扩展配置", max_length=500, default='{}')

    def save(self, *args, **kwargs):
        self.time_updated = now()
        super(UserProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nickname


class UserDetail(models.Model):
    class Meta:
        verbose_name_plural = '详细资料'
        verbose_name = '详细资料'

    uid = models.IntegerField('用户ID', primary_key=True)
    fullname = models.CharField('姓名', max_length=30, blank=True, null=True)

    sex_type = (
        (None, u'未知'),
        (1, u'男'),
        (0, u'女'),

    )
    sex = models.NullBooleanField('性别', choices=sex_type, blank=True, null=True)
    birthday = models.DateField('生日', default=now, blank=True, null=True)
    city = models.CharField('现居城市', max_length=50, blank=True, null=True)
    address = models.CharField('通讯地址', max_length=100, blank=True, null=True)
    homepage = models.URLField('个人网站', max_length=100, blank=True, null=True)
    signature = models.TextField('自我简介', blank=True, null=True)
    time_updated = models.DateTimeField('更新时间', default=now)

    def save(self, *args, **kwargs):
        self.time_updated = now()
        super(UserDetail, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.fullname
