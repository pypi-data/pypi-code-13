import logging
import signal
import subprocess as sp

from test_recorder.os_utils import get_source, get_window, get_screen_size


class VideoRecorder:
    def __init__(self):
        self.process = None
        self.video_enabled = True

    def start_recording(self, filename):
        command = ['ffmpeg',
                   '-y',  # (optional) overwrite output file if it exists
                   '-f', get_source(),  # grab video from source
                   '-video_size', get_screen_size(),  # screen size
                   '-r', '24',  # frames per second
                   '-i', get_window(),  # The input comes from a pipe
                   '-an',
                   filename]

        if self.video_enabled:
            self.process = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

    def stop_recording(self):
        if self.video_enabled:
            self.process.send_signal(signal.SIGINT)
            err = self.process.communicate()
            logging.warning(err)


