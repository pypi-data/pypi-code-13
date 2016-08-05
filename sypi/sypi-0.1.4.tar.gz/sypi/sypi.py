#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sypi import settings
from sypi import utils
from sypi import info

class Sypi():

	def __init__(self, log_path=settings.SYPI_LOG_PATH, logging_level=settings.SYPI_LOGGING_LEVEL):

		self._log_path = log_path
		self._log_file = "{path}/{file_name}.log".format(path=self._log_path, file_name=__name__)
		self._logging_level = logging_level
		self._logger = utils.config_logger(__name__, self._log_file, logging_level=self._logging_level)

		self._logger.debug("{name} object instantiation".format(name=__name__))

	def info(self):

		return info.get_system_info()

	def memory(self):

		return info.get_system_memory()
