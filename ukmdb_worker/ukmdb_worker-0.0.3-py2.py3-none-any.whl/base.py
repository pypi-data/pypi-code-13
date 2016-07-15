#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103

import logging
from schema import SchemaError


def validate(args, test_schema):
    try:
        args = test_schema.validate(args)
        return args
    except SchemaError as e:
        exit(e)


def set_debug_level(logger, arguments):
    if arguments['--debug'] == 1:
        logger.setLevel(logging.WARNING)
        logging.basicConfig()
        logger.warning("Debugging with level: 'WARNING'")
    elif arguments['--debug'] == 2:
        logger.setLevel(logging.INFO)
        logging.basicConfig()
        logger.info("Debugging with level: 'INFO'")
    elif arguments['--debug'] > 2:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig()
        logger.debug("Debugging with level: 'DEBUG'")
    else:
        logger.setLevel(logging.ERROR)
        logging.basicConfig()
