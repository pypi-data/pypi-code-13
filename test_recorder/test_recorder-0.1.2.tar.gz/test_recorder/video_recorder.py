import ctypes
import logging
import signal
import subprocess as sp
import video_config
from test_recorder.os_utils import get_source, get_window, get_screen_size, is_windows, get_process_name


class VideoRecorder:
    last_recording = None

    def __init__(self):
        self.process = None
        self.process_name = get_process_name()

    def start_recording(self, filename):
        VideoRecorder.last_recording = filename
        command = [self.process_name,
                   '-y',  # (optional) overwrite output file if it exists
                   '-f', get_source(),  # grab video from source
                   '-video_size', get_screen_size(),  # screen size
                   '-r', video_config.frames_per_sec,  # frames per second
                   '-i', get_window(),  # The input comes from a pipe
                   '-an',
                   filename]

        if is_windows:
            self.process = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE,
                                    creationflags=512)  # creationflags for windows compatibility. Stacoverflow hint
        else:
            self.process = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

    def stop_recording(self):
        if is_windows:
            self.kill_ffmpeg_win(self.process.pid)
        else:
            ffmpeg_process = self.process
            ffmpeg_process.send_signal(signal.SIGINT)
            err = ffmpeg_process.communicate()  # wait until process finished
            logging.info(err)

    def kill_ffmpeg_win(self, pid):
        logging.info("Trying to kill ffmpeg {}".format(pid))
        ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, pid)  # CTRL_C_EVENT = 0
        logging.info("Killed")
        self.process.terminate()
        self.process.wait()
