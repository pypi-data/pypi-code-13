# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from .models import Keyword, AssignedKeyword


# 同步关键词到M2M表的函数，供 post_save 函数调用
def sync_keywords(string, pk, atype, ctype):
    # 获取关键词id
    # time.sleep(15)
    keywords = string.split(' ')
    if len(keywords):
        # 获取模型id
        cmod = ContentType.objects.get(app_label=atype, model=ctype)
        content_id = cmod.id
        # 已存在的关键词
        existing_objs = AssignedKeyword.objects.filter(content_type=content_id, object_pk=pk)
        existing_list = [key.keyword_id for key in existing_objs]
        # 删除多余的关键词
        for e_obj in existing_objs:
            if e_obj.keyword.title not in keywords:
                existing_objs.filter(id=e_obj.id).delete()
        # 添加新关键词
        order = -1
        for ky in keywords:
            if len(ky):
                order += 1
                # 下面有魔法，请勿轻易改动，非池
                key1_objs = Keyword.objects.filter(title__exact=ky)
                key2_objs = Keyword.objects.filter(title__exact=str(ky.encode('utf8')))
                key_obj = key2_objs[0] if len(key2_objs) else None
                if key_obj is None and len(key1_objs):
                    key_obj = key1_objs[0]
                if key_obj is not None:
                    if key_obj.id not in existing_list:
                        new_data = {'content_type': cmod, 'object_pk': pk, 'keyword': key_obj, '_order': order}
                        AssignedKeyword.objects.create(**new_data)
                    else:
                        new_data = {'_order': order}
                        existing_objs.filter(keyword=key_obj.id).update(**new_data)
                # 新建关键词
                else:
                    new_data = {'title': ky}
                    new_obj = Keyword.objects.create(**new_data)
                    new_assign = {'content_type': cmod, 'object_pk': pk, 'keyword': new_obj, '_order': order}
                    AssignedKeyword.objects.create(**new_assign)
