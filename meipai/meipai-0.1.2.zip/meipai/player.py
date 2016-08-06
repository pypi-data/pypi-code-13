import os, sys
import subprocess

from meipai.cache import CACHE_PATH

__author__ = 'PyBeaner'


class Player:
    def __init__(self):
        pass

    @staticmethod
    def play(url):
        if sys.platform.startswith('win'):
            process = os.system('start wmplayer.exe ' + url)
        else:
            process = subprocess.Popen(args=('open', '-a', 'QuickTime Player', url), stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process = os.startfile('url')
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
    Player.play(video)
    assert (Player.played(video) is True)
