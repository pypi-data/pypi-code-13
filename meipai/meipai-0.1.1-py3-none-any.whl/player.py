import os
import subprocess

from src.cache import CACHE_PATH

__author__ = 'PyBeaner'


class Player:
    def __init__(self):
        pass

    @staticmethod
    def play(url):
        process = subprocess.Popen(args=('open', '-a', 'QuickTime Player', url), stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process = subprocess.Popen(args=('mplayer', url), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                            stderr=subprocess.PIPE)
        open(Player._history_file(), 'a').write(url + os.linesep)
        return process

    @staticmethod
    def played(url):
        if not os.path.exists(Player._history_file()):
            return False
        for line in open(Player._history_file()):
            if line.strip() == url:
                return True

    @staticmethod
    def _history_file():
        return os.path.join(CACHE_PATH, 'play_history.log')


if __name__ == '__main__':
    video = 'http://mvvideo2.meitudata.com/5781ae068dbc86730.mp4'
    # Player.play(video)
    assert (Player.played(video) is True)
