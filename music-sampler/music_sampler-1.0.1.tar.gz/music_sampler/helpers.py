# -*- coding: utf-8 -*-
import argparse
import sys
import os
import math
import sounddevice as sd
import logging

from . import sysfont

class Config:
    pass

def find_font(name, style=sysfont.STYLE_NONE):
    if getattr(sys, 'frozen', False):
        font = sys._MEIPASS + "/fonts/{}_{}.ttf".format(name, style)
    else:
        font = sysfont.get_font(name, style=style)
        if font is not None:
            font = font[4]
    return font

def register_fonts():
    from kivy.core.text import LabelBase

    ubuntu_regular = find_font("Ubuntu", style=sysfont.STYLE_NORMAL)
    ubuntu_bold = find_font("Ubuntu", style=sysfont.STYLE_BOLD)
    symbola = find_font("Symbola")

    if ubuntu_regular is None:
        error_print("Font Ubuntu regular could not be found, please install it.")
        sys.exit()
    if symbola is None:
        error_print("Font Symbola could not be found, please install it.")
        sys.exit()
    if ubuntu_bold is None:
        warn_print("Font Ubuntu Bold could not be found.")

    LabelBase.register(name="Ubuntu",
            fn_regular=ubuntu_regular,
            fn_bold=ubuntu_bold)
    LabelBase.register(name="Symbola",
            fn_regular=symbola)


def path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS + "/"
    else:
        return os.path.dirname(os.path.realpath(__file__))

def parse_args():
    argv = sys.argv[1 :]
    sys.argv = sys.argv[: 1]
    if "--" in argv:
        index = argv.index("--")
        kivy_args = argv[index+1 :]
        argv = argv[: index]

        sys.argv.extend(kivy_args)

    parser = argparse.ArgumentParser(
            description="A Music Sampler application.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--config",
            default="config.yml",
            required=False,
            help="Config file to load")
    parser.add_argument("-p", "--music-path",
            default=".",
            required=False,
            help="Folder in which to find the music files")
    parser.add_argument("-d", "--debug",
            nargs=0,
            action=DebugModeAction,
            help="Print messages in console")
    parser.add_argument("-m", "--builtin-mixing",
            action="store_true",
            help="Make the mixing of sounds manually\
                    (do it if the system cannot handle it correctly)")
    parser.add_argument("-l", "--latency",
            default="high",
            required=False,
            help="Latency: low, high or number of seconds")
    parser.add_argument("-b", "--blocksize",
            default=0,
            type=int,
            required=False,
            help="Blocksize: If not 0, the number of frames to take\
                    at each step for the mixer")
    parser.add_argument("-f", "--frame-rate",
            default=44100,
            type=int,
            required=False,
            help="Frame rate to play the musics")
    parser.add_argument("-x", "--channels",
            default=2,
            type=int,
            required=False,
            help="Number of channels to use")
    parser.add_argument("-s", "--sample-width",
            default=2,
            type=int,
            required=False,
            help="Sample width (number of bytes for each frame)")
    parser.add_argument("-V", "--version",
            action="version",
            help="Displays the current version and exits. Only use\
                    in bundled package",
            version=show_version())
    parser.add_argument("--device",
            action=SelectDeviceAction,
            help="Select this sound device"
            )
    parser.add_argument("--list-devices",
            nargs=0,
            action=ListDevicesAction,
            help="List available sound devices"
            )
    parser.add_argument('--',
            dest="args",
            help="Kivy arguments. All arguments after this are interpreted\
                    by Kivy. Pass \"-- --help\" to get Kivy's usage.")

    from kivy.logger import Logger
    Logger.setLevel(logging.WARN)

    args = parser.parse_args(argv)

    Config.yml_file = args.config

    Config.latency = args.latency
    Config.blocksize = args.blocksize
    Config.frame_rate = args.frame_rate
    Config.channels = args.channels
    Config.sample_width = args.sample_width
    Config.builtin_mixing = args.builtin_mixing
    if args.music_path.endswith("/"):
        Config.music_path = args.music_path
    else:
        Config.music_path = args.music_path + "/"

class DebugModeAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        from kivy.logger import Logger
        Logger.setLevel(logging.DEBUG)

class SelectDeviceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        sd.default.device = values

class ListDevicesAction(argparse.Action):
    nargs = 0
    def __call__(self, parser, namespace, values, option_string=None):
        print(sd.query_devices())
        sys.exit()

def show_version():
    if getattr(sys, 'frozen', False):
        with open(path() + ".pyinstaller_commit", "r") as f:
            return f.read()
    else:
        return "option '-v' can only be used in bundled package"

def duration_to_min_sec(duration):
    minutes = int(duration / 60)
    seconds = int(duration) % 60
    if minutes < 100:
        return "{:2}:{:0>2}".format(minutes, seconds)
    else:
        return "{}:{:0>2}".format(minutes, seconds)

def gain(volume, old_volume=None):
    if old_volume is None:
        return 20 * math.log10(max(volume, 0.1) / 100)
    else:
        return [
                20 * math.log10(max(volume, 0.1) / max(old_volume, 0.1)),
                max(volume, 0)]

def debug_print(message, with_trace=False):
    from kivy.logger import Logger
    Logger.debug('MusicSampler: ' + message, exc_info=with_trace)

def error_print(message, with_trace=False):
    from kivy.logger import Logger
    Logger.error('MusicSampler: ' + message, exc_info=with_trace)

def warn_print(message, with_trace=False):
    from kivy.logger import Logger
    Logger.warn('MusicSampler: ' + message, exc_info=with_trace)

