import functools
import inspect
import os

import wrapt as wrapt

import video_config
from time import strftime

from test_recorder.file_utils import create_dir
from test_recorder.os_utils import get_file_format
from test_recorder.video_recorder import VideoRecorder


def video(wrapped=None, enabled=True):
    if wrapped is None:
        return functools.partial(video, enabled=enabled)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        if enabled:
            Video.record(wrapped, *args, **kwargs)
        else:
            wrapped(*args, **kwargs)

    return wrapper(wrapped)


def video_recorder(decorator, prefix='test_'):
    def wrapper(cls):
        for name, m in inspect.getmembers(cls, inspect.ismethod):
            if name.startswith(prefix):
                setattr(cls, name, decorator(m))
        return cls

    return wrapper


class Video(object):
    @staticmethod
    def record(func, *args, **kwargs):
        file_path = Video._get_file_path(func)
        recorder = VideoRecorder()
        recorder.start_recording(file_path)
        passed = False
        try:
            func(*args, **kwargs)
            passed = True
        finally:
            recorder.stop_recording()
        if passed:
            os.remove(file_path)

    @staticmethod
    def _get_file_path(func):
        dir_path = video_config.dir_path
        create_dir(dir_path)  # create video folder if not exists
        file_name = '{0}_{1}.{2}'.format(func.func_name,
                                         strftime("%Y_%m_%d_%H_%M_%S"), get_file_format())  # format timestamp
        return dir_path + os.sep + file_name  # save file to user_home/video directory
