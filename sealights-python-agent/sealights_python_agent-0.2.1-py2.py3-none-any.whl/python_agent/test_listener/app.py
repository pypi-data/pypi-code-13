import logging

log = logging.getLogger(__name__)


def main():
    try:
        arguments = None  # parse user args

    except Exception as e:
        log.exception("failed running test listener. error: %s" % str(e))

