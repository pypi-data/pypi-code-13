import nicecall


class NullProcess(nicecall.Process):
    def execute(self):
        return 0
