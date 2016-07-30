from .print_it import PrintIt


class Rt(object):
    def __init__(self):
        pass

    @staticmethod
    def just_print(text: str):
        print(text)
        PrintIt().print_it(text)

Rt.just_print('RT')
