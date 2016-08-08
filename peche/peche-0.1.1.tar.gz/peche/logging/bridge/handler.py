import logging
from peche.logging import Level
from peche.logging.handlers import Handler

class BridgeHandler(Handler):

    def __init__(self, logger):
        super().__init__()

        self.logger = logger

    def emit(self, record):
        self.logger._log(
            Level(record.levelno),
            record.getMessage()
        )