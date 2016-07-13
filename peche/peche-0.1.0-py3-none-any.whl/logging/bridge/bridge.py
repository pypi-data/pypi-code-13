import logging
from peche.logging.bridge.handler import BridgeHandler as Bridge
import peche.manager

def bridge(name, logger=None):
    if logger is None:
        _, logger = peche.manager.Manager().setup(name=name)

    log = logging.getLogger(name)

    log.handlers = []
    log.level = logger.level.value

    log.addHandler(Bridge(logger))