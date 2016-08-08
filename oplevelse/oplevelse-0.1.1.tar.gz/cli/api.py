import os
import json
import errno
import zipfile
import requests
import StringIO


class APIBase(object):
	def __init__(self, home, api_url, token, config, debug, **kwargs):
		self.home = os.path.realpath(os.path.expanduser(home))
		self.api_url = api_url
		self.config = os.path.realpath(os.path.expanduser(config))
		self.debug = debug

		self.try_read_config(token)

	def _build_url(self, url):
		return requests.compat.urljoin(self.api_url, url)

	def _headers(self):
		return {
			'Authorization': 'token %s' % (self.token)
		}

	def _call(self, url, method, **kwargs):
		kwargs['headers'] = self._headers()

		method = getattr(requests, method)

		response = method(self._build_url(url), **kwargs)
		response.raise_for_status()
		return response

	def _get(self, url, data={}):
		return self._call(url, 'get', params=data)

	def _post(self, url, data={}):
		return self._call(url, 'post', data=data)


class LangAPIMixin():
	def lang_list(self):
		return self._get(self._build_url('/api/v1/lang/')).json()


class TaskAPIMixin():
	def task_list(self, lang):
		return self._get(self._build_url('/api/v1/task/'), {'lang': lang}).json()

	def has_task(self, lang, task):
		try:
			self._get(self._build_url('/api/v1/task/%s-%s' % (lang, task, )))
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 404:
				return False
			else:
				raise
		else:
			return True

	def task_get(self, lang, task):
		task = self._get(self._build_url('/api/v1/task/%s-%s/' % (lang, task, ))).json()

		zip = zipfile.ZipFile(
			StringIO.StringIO(
				requests.get(task.get('content'), stream=True).content
			)
		)

		path = os.path.join(os.path.expanduser(self.home), lang, task.get('name'))

		try:
			os.makedirs(path)
		except OSError as exc:
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else:
				raise

		zip.extractall(path)


class AuthMixin():
	def login(self, github_token):
		return self._post(self._build_url('api-token-auth/'), {
			'github_token': github_token
		}).json()


class StatsMixin():
	def stats(self):
		return self._get(self._build_url('/stats/')).json()


class SolutionMixin():
	def persist_token(self, token):
		with open(self.config, 'w') as f:
			f.write(json.dumps(dict(token=token)))

	def try_read_config(self, default=None):
		if os.path.isfile(self.config):
			with open(self.config, 'r') as f:
				self.token = json.loads(f.read()).get('token')
		else:
			self.token = default

	def submit(self, lang, task, files):
		in_memory = StringIO.StringIO()
		zip = zipfile.ZipFile(in_memory, "a")

		for file in files:
			zip.write(file.path, file.rel)

			for f in zip.filelist:
				f.create_system = 0

		zip.close()
		in_memory.seek(0)

		try:
			response = requests.post(self._build_url('/api/v1/submit/'), files={
				'content': in_memory.read()
			}, data={
				'lang': lang,
				'task': task,
			}, headers=self._headers())

			response.raise_for_status()

			return response.json()
		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 401:
				from oplevelse import oplevelse
				raise oplevelse.NotAuthorized()
			else:
				raise


class OplevelseAPI(APIBase, LangAPIMixin, TaskAPIMixin, SolutionMixin, AuthMixin, StatsMixin):
	pass
