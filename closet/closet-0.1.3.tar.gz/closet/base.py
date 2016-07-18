import os

import magic

from exceptions import (
    FileNotFoundError,
    )


class StorageServiceBase(object):
    def __init__(self, name=None, bucket=None, *args, **kwargs):
        self.name = name or 'default'
        self.bucket = bucket or (self.name if bucket is None else None)

    def _normalize_path(self, filename):
        if self.bucket:
            filename = os.path.join(self.bucket, filename)
        filename = os.path.normpath(filename)
        return filename

    def exists(self, filename):
        raise NotImplementedError()

    def open(self, filename, mode=None):
        raise NotImplementedError()

    def stat(self, filename):
        raise NotImplementedError()

    def delete(self, filename):
        raise NotImplementedError()

    def mimetype(self, filename):
        return self.open(filename, mode='rb').mimetype

    @staticmethod
    def mimetype_for(file_obj):
        if not hasattr(file_obj, '_mimetype'):
            pos = file_obj.tell()
            file_obj.seek(0)
            file_obj._mimetype = magic.from_buffer(file_obj.read(1024), mime=True)
            file_obj.seek(pos)
        return file_obj._mimetype


class FileStat(object):
    def __init__(self, size, atime, mtime, ctime):
        self.size = size
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
