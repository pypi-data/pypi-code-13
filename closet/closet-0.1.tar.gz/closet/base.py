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


class FileProxy(object):
    def __init__(self, file_obj):
        self.file_obj = file_obj

    def __getattr__(self, key):
        return getattr(self.file_obj, key)

    def __setattr__(self, key, value):
        return setattr(self.file_obj, key, value)

    @property
    def mimetype(self):
        if not hasattr(self, '_mimetype'):
            pos = self.tell()
            self.seek(0)
            self._mimetype = magic.from_buffer(self.read(1024), mime=True)
            self.seek(pos)
        return self._mimetype


class FileStat(object):
    def __init__(self, size, atime, mtime, ctime):
        self.size = size
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
