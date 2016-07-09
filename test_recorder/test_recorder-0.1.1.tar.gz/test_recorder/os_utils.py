import platform
import ctypes
import Tkinter

is_windows = platform.system() == 'Windows'
is_mac = platform.system() == 'Darwin'


def get_source():
    if is_mac:
        return 'avfoundation'
    elif is_windows:
        return 'gdigrab'
    else:
        return 'x11grab'


def get_window():
    return 'desktop' if is_windows else ':0.0'


def get_screen_size():
    if is_windows:
        user32 = ctypes.windll.user32
        return __format(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    else:
        root = Tkinter.Tk()
        return __format(root.winfo_screenwidth(), root.winfo_screenheight())


def __format(screen_width, screen_height):
    return '{0}x{1}'.format(screen_width, screen_height)
