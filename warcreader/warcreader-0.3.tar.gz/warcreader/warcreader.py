# Copyright 2016 Milos Svana
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

class Webpage(object):
	'''
	Represents one webpage (or HTTP response) from WARC file. You can access:
	- payload: HTML source code of the page for example
	- uri: absolute URI
	- content_type: value of HTTP header Content-Type field
	'''

	def __init__(self, warc_record, uri, payload, content_type):
		''' Called by WarcFile '''
		self.uri = uri
		self.payload = payload
		self.content_type = content_type
		self.warc_record = warc_record

class WarcFile(object):
	'''
	Reads the web achive (WARC) files. 
	Can iterate through HTTP responses inside using a simple state machine.
	'''

	http_response_re = re.compile(b'^HTTP\/1\.[01] 200')
	warc_header_re = re.compile(b'^WARC\/[0-9\.]+(\r)?\n$')
	h_letter = b'H'
	w_letter = b'W'

	def __init__(self, file_object):
		'''
		Accepts a file object or any other object which provides same interface,
		for example an instance of gzip.GzipFile class. This object should 
		contain the WARC archieve. The file must be opened in binary mode.

		Sets the initial state of the state machine.
		'''
		self.file_object = file_object
		self.init_state()

	def __iter__(self):
		''' Make object iterable. '''
		return self

	def next(self):
		return self.__next__()

	def __next__(self):
		''' Returns next HTTP response from the WARC file. '''
		content_type = uri = None
		for line in self.file_object:
			if not self.in_warc_response:
				if line[:19] == b'WARC-Type: response':
					warc_record_lines = [self.prev_line, line]
					self.in_warc_response = True
				self.prev_line = line
				continue
			warc_record_lines.append(line)
			if not self.in_http_response:
				if line[:11] == b'WARC-Target':
					uri_end = -2 if line[-2] == '\r' else -1
					uri = line[17:uri_end]
				elif line[0:1] == self.h_letter and self.http_response_re.match(line):
					self.in_http_response = True
				continue
			if not self.in_payload:
				if line[:13] == b'Content-Type:':
					content_type = line[14:-2]
				elif line == b'\r\n':
					payload_lines = []
					self.in_payload = True
				continue
			if line[0:1] == self.w_letter and self.warc_header_re.match(line):
				payload = b''.join(payload_lines[:-2])
				warc_record = b''.join(warc_record_lines[:-2])
				self.prev_line = line
				self.init_state()
				return Webpage(warc_record, uri, payload, content_type)
			payload_lines.append(line)
		raise StopIteration()

	def init_state(self):
		''' Sets the initial state of the state machine. '''
		self.in_warc_response = False
		self.in_http_response = False
		self.in_payload = False
