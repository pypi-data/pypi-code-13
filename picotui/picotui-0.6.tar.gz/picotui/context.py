from .screen import Screen

class Context:

    def __enter__(self):
        Screen.init_tty()
        Screen.enable_mouse()
        Screen.cls()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Screen.goto(0, 50)
        Screen.cursor(True)
        Screen.deinit_tty()
