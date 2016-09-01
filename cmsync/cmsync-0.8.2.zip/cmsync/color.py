import colorama

colorama.init()


class Color:
    """
    Codeminus' color constants
    """
    ERROR = colorama.Fore.LIGHTRED_EX
    WARNING = colorama.Fore.LIGHTYELLOW_EX
    INFO = colorama.Fore.LIGHTCYAN_EX
    COMMAND = colorama.Fore.LIGHTWHITE_EX
