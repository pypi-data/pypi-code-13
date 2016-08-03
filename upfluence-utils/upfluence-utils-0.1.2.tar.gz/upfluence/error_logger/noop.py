import upfluence.log


class Client(object):
    def __init__(self):
        self.extra = {}

    def capture_exception(*args, **kwargs):
        upfluence.log.logger.error('exception:', exc_info=True)
