import os
import zipfile
import requests
import StringIO


class APIBase():
	def __init__(self, home, api_server, debug=False):
		self.home = home
		self.api_server = api_server
		self.debug = debug

	def build_url(self, url):
		return requests.compat.urljoin(self.api_server, url)


class LangAPI(APIBase):
	def list(self):
		langs = requests.get(self.build_url('/api/v1/lang/'))
		langs.raise_for_status()
		return langs.json()


class TaskAPI(APIBase):
	def list(self, lang):
		langs = requests.get(self.build_url('/api/v1/task/'), {'lang': lang})
		langs.raise_for_status()
		return langs.json()

	def get(self, lang, task):
		task = requests.get(self.build_url('/api/v1/task/%s-%s' % (lang, task, )))
		task.raise_for_status()

		task = task.json()
		zip = zipfile.ZipFile(StringIO.StringIO(requests.get(task.get('content'), stream=True).content))

		root = os.path.expanduser(self.home)
		lang_root = os.path.join(root, lang)
		task_root = os.path.join(lang_root, task.get('name'))

		if not os.path.exists(lang_root):
			os.makedirs(lang_root)
			os.makedirs(task_root)

		zip.extractall(task_root)


class OplevelseAPI():
	def __init__(self, *args, **kwargs):
		self.lang = LangAPI(*args, **kwargs)
		self.task = TaskAPI(*args, **kwargs)
