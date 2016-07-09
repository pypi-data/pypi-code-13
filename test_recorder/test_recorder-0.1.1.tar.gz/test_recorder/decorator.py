import functools
import inspect
import os
from os.path import expanduser
from time import strftime

from test_recorder.file_utils import create_dir
from test_recorder.video_recorder import VideoRecorder


def video(enabled=True):
    def video_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            file_path = get_file_path(func)
            recorder = VideoRecorder()
            recorder.video_enabled = enabled
            recorder.start_recording(file_path)
            try:
                func(*args, **kwargs)
                os.remove(file_path)
            finally:
                recorder.stop_recording()

        return wrapper

    def get_file_path(func):
        dir_path = expanduser("~") + os.sep + 'video'  # video folder path
        create_dir(dir_path)  # create video folder if not exists
        file_name = '{0}_{1}.mp4'.format(func.func_name,
                                         strftime("%Y_%m_%d_%H_%M_%S"))  # format timestamp
        return dir_path + os.sep + file_name  # save file to user_home/video directory

    return video_decorator


def video_recorder(decorator, prefix='test_'):
    def wrapper(cls):
        for name, m in inspect.getmembers(cls, inspect.ismethod):
            if name.startswith(prefix):
                setattr(cls, name, decorator(m))
        return cls

    return wrapper
