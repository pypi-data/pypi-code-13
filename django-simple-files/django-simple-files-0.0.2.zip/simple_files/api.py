# -*- coding: UTF-8 -*-
import logging
import os

from simple_files import models
from simple_files import settings
from simple_files import utils

logger = logging.getLogger('django')


def _get_file_hash(content):
    hash_fun = settings.get_file_fun_name()
    if hash_fun == "CRC32":
        return utils.crc32(content)
    else:
        return utils.md5(content)


def file_save(name, content, uploader_uid=0):
    """
    保存文件，同时保存文件至数据库
    :param name:
    :param content:
    :param uploader_uid:
    :return:
    """
    file_db = models.Files()
    file_db.file_hash = _get_file_hash(content)
    file_db.file_size = len(content)
    file_db.uploader_uid = uploader_uid
    file_name = utils.storage_save(name, content, file_db.file_uri)
    file_db.file_uri.name = file_name
    file_db.save()
    return file_db


def file_save_by_hash(name, content, uploader_uid=0):
    """
    随机生成文件名保存
    :param content:
    :param uploader_uid:
    :return:
    """
    hash_name = utils.hash_uuid()
    file_ext = os.path.splitext(name)[-1]
    return file_save(hash_name + file_ext, content, uploader_uid)


def file_related_save(file_db, related_object):
    """
    保存关系表
    :param file_db:
    :param related_object:
    :return:
    """
    file_related = models.FilesRelated()
    file_related.file = file_db
    file_related.file_uri = file_db.file_uri
    file_related.related_object_id = related_object.pk
    file_related.related_object = utils.get_object_name(related_object)
    file_related.save()
    return file_related


def _file_related_filter(related_object_name, related_object_id=None, file_id=0):
    query = {'related_object': related_object_name}
    if related_object_id:
        query['related_object_id'] = related_object_id
    if file_id:
        query['file_id'] = file_id
    return models.FilesRelated.objects.filter(**query)


def _file_related_filter_by_object(related_object, file_id=0):
    related_object_name = utils.get_object_name(related_object)
    related_object_id = related_object.pk if hasattr(related_object, 'pk') else None
    return _file_related_filter(related_object_name, related_object_id, file_id)


def file_related_get_by_object(related_object, page=1, page_size=20):
    """
    根据对象名与对象pk返回相关数据
    :param related_object:
    :param page:
    :param page_size:
    :return:
    """
    return _file_related_filter_by_object(related_object)[(page-1)*page_size:page_size]


def file_related(related_object, page=1, page_size=20):
    """
    根据对象名返回相关数据
    :param related_object:
    :param page:
    :param page_size:
    :return:
    """
    return _file_related_filter(utils.get_object_name(related_object))[(page-1)*page_size:page_size]


def file_related_delete_by_object(related_object):
    _file_related_filter(related_object).delete()
