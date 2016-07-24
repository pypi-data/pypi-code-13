# -*- coding: UTF-8 -*-

import base64
import binascii
import hashlib
import logging
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

logger = logging.getLogger('django')


def crc32(file_blob):
    """
    从进制获取文件crc32信息
    :param file_blob:
    :return:
    """
    crc_code = binascii.crc32(file_blob)
    if crc_code > 0:
        crc_int = crc_code
    else:
        crc_int = ~ crc_code ^ 0xffffffff
    return '%x' % crc_int


def crc32_from_path(file_path):
    """
    从路径文件crc32信息
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as f:
        return crc32(f.read())


def blob_from_h5base64(blob_from_h5base64_data):
    """
    从前端预览上传的Base64编码获取data数据
    :param blob_from_h5base64_data:
    :return:
    """
    return blob_from_base64(blob_from_h5base64_data.split(',')[-1])


def blob_from_base64(base64_data):
    """
    从Base64完整data中获取二进制data数据
    :param base64_data:
    :return:
    """
    return base64.b64decode(base64_data)


def md5(file_blob):
    """
    从二进制对象获取md5信息
    :param file_blob:
    :return:
    """
    return hashlib.md5(file_blob).hexdigest()


def md5_from_path(file_path):
    """
    从文件获取md5信息
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as f:
        return md5(f.read())


def storage_save(name, content, storage=None):
    """
    使用django storage 保存文件
    :param name:
    :param content:
    :param storage:
    :return:
    """
    if not storage:
        storage = default_storage
    return storage.save(name, ContentFile(content))


def storage_exists(name):
    return default_storage.exists(name)


def hash_uuid():
    return str(uuid.uuid1()).replace('-', '')


def get_object_name(obj):
    return '%s.%s' % (obj.__module__, obj.__class__.__name__)


