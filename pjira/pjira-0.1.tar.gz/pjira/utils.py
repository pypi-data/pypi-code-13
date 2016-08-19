from os.path import expanduser
import os
import json
import editor
import re

class ConfigManager(object):
	"Manages Client connection details"
	def __init__(self):
		pass

	@classmethod
	def prepare_config_dir(cls):
		home  = os.path.join(expanduser("~"),  ".jira")
		if not os.path.exists(home):
			os.makedirs(home)
		return home

	@classmethod
	def get_config_file_name(cls):
		home = cls.prepare_config_dir()
		return os.path.join(home, "config.json")

	@classmethod
	def save_details(cls, host, user, password):
		config_file = cls.get_config_file_name();
		details = {'user': user, 'host':host, 'password':password}
		save_json_to_file(details, config_file)

	@classmethod
	def _check_config(cls, json_obj):
		for key in ['user', 'host', 'password']:
			if key not in json_obj:
				return False
		return True

	@classmethod	
	def get_details(cls):
		config_file = cls.get_config_file_name();
		try:
			json_obj = get_json_from_file(config_file)
			if not cls._check_config(json_obj):	
				raise InvalidConfiguration("Invalid configuration")
		except IOError:
			raise InvalidConfiguration("Configuration file doesnt exists")
		except ValueError:
			raise InvalidConfiguration("Invalid configuration")
		return json_obj

issue_template = """##Summary##
 Write Summary Here
##End##
##Description##
 Write Description Here
##End##
"""
issue_regex = r'##Summary##(?P<summary>(.|\n)*)\n##End##\n##Description##(?P<desc>(.|\n)*)\n##End##'
comment_template = """
****** Comment ******
 Write Comment Here
****** End ******
"""
class EditorMode(object):
	def __init__(self, type):
		self.type = type

	def open(self):
		template = issue_template if self.type == 'issue' else comment_template
		self.value = editor.edit(contents=template)

	def _parse_issue_template(self):
		text = self.value
		reg_search = re.search(issue_regex, text)
		data = reg_search.groupdict()
		summary = data['summary'];
		description = data['desc'];
		return {'summary':summary, 'description':description}

	def parse(self):
		return self._parse_issue_template() if self.type == 'issue' else self._parse_comment_template()

	def get(self):
		return self.parse(self.value)


class InvalidConfiguration(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def ask_for_confirmation(text):
	while True:
		res = str(input(text))
		if res.lower() not in ['y', 'n']:
			print 'Please try with a valid response'
			continue
		else:
			return res.lower() == 'y'



def save_json_to_file(json_obj, file):
	with open(file, 'w') as config:
		config.write(json.dumps(json_obj))


def get_json_from_file(file):
	with open(file, 'r') as config:
		return json.loads(config.read())
