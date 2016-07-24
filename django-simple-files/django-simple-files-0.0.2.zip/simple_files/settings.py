# -*- coding: UTF-8 -*-
import os

from django.conf import settings
from django.core.files.storage import default_storage

# django.core.files.storage.FileSystemStorage

print(default_storage)

SIMPLE_FILES = {
    'FILE_HASH_FUN': 'MD5',
    'FILE_UPLOAD_TO': 'upload/%Y%m%d%H%M%S',
    'FILE_LOCAL_BACKUP': False,
    'FILE_LOCAL_BACKUP_DIR': os.path.join(settings.BASE_DIR, 'storage/backup')
}


def get_setting_value(name):
    simple_files_name = 'SIMPLE_FILES'
    if hasattr(settings, simple_files_name):
        simple_files_dict = getattr(settings, simple_files_name)
        if isinstance(simple_files_dict, dict):
            return simple_files_dict.get(name) or SIMPLE_FILES.get(name)


def get_file_fun_name():
    file_hash_fun_key = 'FILE_HASH_FUN'
    file_hash_fun = get_setting_value(file_hash_fun_key)
    return file_hash_fun if file_hash_fun and file_hash_fun == 'CRC32' else SIMPLE_FILES.get(file_hash_fun_key)


def get_upload_to():
    file_upload_to_key = 'FILE_UPLOAD_TO'
    upload_to = get_setting_value(file_upload_to_key)
    return upload_to if upload_to else SIMPLE_FILES.get(file_upload_to_key)
