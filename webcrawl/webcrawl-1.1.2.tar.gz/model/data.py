#!/usr/bin/env python
# coding=utf-8
import datetime
from setting import baseorm, dataorm

class MarkModel(dataorm.Model):
    create_time = dataorm.DatetimeField(ddl='datetime', updatable=False)
    update_time = dataorm.DatetimeField(ddl='timestamp')
    tid = baseorm.IdField(unique='data', updatable=False)

    def __init__(self, **attributes):
        # self.__mappings__['create_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['update_time'] = dataorm.DatetimeField(ddl='datetime')
        # self.__mappings__['tid'] = baseorm.IdField(unique='data', updatable=False)
        attributes['create_time'] = attributes.get('create_time', datetime.datetime.now())
        attributes['update_time'] = attributes.get('update_time', datetime.datetime.now())
        for key in self.__mappings__:
            if key == '_id' and not key in attributes:
                continue
            if not key in attributes:
                raise Exception('Need field %s. ' % key)
            attributes[key] = self.__mappings__[key].check_value(attributes[key])
        print '_______'
        super(MarkModel, self).__init__(**attributes)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__



'''
@comment('音频数据')
'''
class Audio(MarkModel):
    __table__ = 'audio'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    url = dataorm.StrField(ddl='str', comment='资源地址')
    format = dataorm.StrField(ddl='str', comment='资源格式')
    size = dataorm.IntField(ddl='int', comment='资源大小')
    during = dataorm.IntField(ddl='int', comment='资源时长')
    tag = dataorm.ListField(ddl='list', comment='资源标签')
    name = dataorm.StrField(ddl='str', comment='资源名称')
    desc = dataorm.StrField(ddl='str', comment='资源描述')
    cover = dataorm.StrField(ddl='str', comment='资源封面')
    singer = dataorm.StrField(ddl='str', comment='资源歌手')
    snum = dataorm.IntField(ddl='int', comment='资源序号')
    src = dataorm.StrField(ddl='str', comment='资源来源')
    host = dataorm.StrField(ddl='str', comment='资源域名')
    page_url = dataorm.StrField(ddl='str', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', unique='data', updatable=False, comment='资源页面id')
    parent_page_id = dataorm.IntField(ddl='int', comment='资源父页面id')
    atime = dataorm.DatetimeField(ddl='datetime', comment='资源来源时间')

'''
@comment('test数据')
'''
class Test(MarkModel):
    __table__ = 'test'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    url = dataorm.StrField(ddl='str', comment='资源地址')
    format = dataorm.StrField(ddl='str', comment='资源格式')
    size = dataorm.IntField(ddl='int', comment='资源大小')
    during = dataorm.IntField(ddl='int', comment='资源时长')
    tag = dataorm.ListField(ddl='list', comment='资源标签')
    name = dataorm.StrField(ddl='str', comment='资源名称')
    desc = dataorm.StrField(ddl='str', comment='资源描述')
    cover = dataorm.StrField(ddl='str', comment='资源封面')
    singer = dataorm.StrField(ddl='str', comment='资源歌手')
    snum = dataorm.IntField(ddl='int', comment='资源序号')
    src = dataorm.StrField(ddl='str', comment='资源来源')
    host = dataorm.StrField(ddl='str', comment='资源域名')
    page_url = dataorm.StrField(ddl='str', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', unique='data', updatable=False, comment='资源页面id')
    parent_page_id = dataorm.IntField(ddl='int', comment='资源父页面id')
    atime = dataorm.DatetimeField(ddl='datetime', comment='资源来源时间')

'''
@comment('test page数据')
'''
class TestPage(MarkModel):
    __table__ = 'test_page'
    cat = dataorm.ListField(ddl='list', comment='资源分类')
    page_url = dataorm.StrField(ddl='str', unique='data', comment='资源原页面地址')
    page_id = dataorm.IntField(ddl='int', updatable=False, comment='资源页面id')
    atime = dataorm.DatetimeField(ddl='datetime', comment='资源来源时间')

if __name__ == '__main__':
    pass


