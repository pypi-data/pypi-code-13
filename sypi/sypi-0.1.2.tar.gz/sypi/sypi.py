#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sypi import info

class Sypi():

	def info(self):

		return info.get_system_info()

	def memory(self):

		return info.get_system_memory()