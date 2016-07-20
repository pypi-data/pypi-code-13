# coding=utf-8
"""
说明: 进行测试的文件
作者:pengxin.wu 15645060726@163.com
创建时间: 2016-7-3
"""
from manager import REDIS_CONNECT_SET
from __init__ import *


class TestModel(RedisModel):
    name = CharField(name="aaa", max_length=100)
    age = IntField(default=12)


class Blog(RedisModel):
    title = CharField(max_length=110, default="tittle_default")
    auther = CharField()
    click = IntField()

    class Meta:
        app_name = "wupeaking2"


if __name__ == "__main__":
    REDIS_CONNECT_SET.update(dict(db=4, password="123456"))

    # import uuid
    # import random
    # for i in xrange(10):
    #     blog = Blog.objects.create(title=str(uuid.uuid1()), auther="mew man%s"%i, click=10)
    # authers = ["liu dehua", "maliya", "小泽", "花木", "曾工", "kitty", "刘东方"]
    # for i in xrange(100):
    #     blog = Blog.objects.create(title=str(uuid.uuid1()), auther=authers[random.randrange(0, len(authers))],
    #                                click=1000*random.random())
    ret = Blog.objects.delete(id=32)
    print ret

    #
    # try:
    #     ret = Blog.objects.get(auther="刘东方")
    # except Blog.DoesNotExits:
    #     print "不存在"
    #
    # ret = Blog.objects.filter(id=100)
    # for i in ret:
    #     print i.title
    #     print i.auther
    #     print i.click
    #     print i.id
