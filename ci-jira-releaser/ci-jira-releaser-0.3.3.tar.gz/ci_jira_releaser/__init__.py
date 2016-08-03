from __future__ import print_function
try:
	from jira import JIRA
except ImportError:
	print('Please install jira with pip install jira')
try:
	from git import Repo
except ImportError:
	print('Please install gitpython with pip install gitpython')
try:
	import requests
except ImportError:
	print('Please install requests with pip install requests')

import re
import os
from datetime import datetime
import random

left = ["happy", "jolly", "dreamy", "sad", "angry", "pensive", "focused", "sleepy", "grave", "distracted", "determined", "stoic", "stupefied", "sharp", "agitated", "cocky", "tender", "goofy", "furious", "desperate", "hopeful", "compassionate", "silly", "lonely", "condescending", "naughty", "kickass", "drunk", "boring", "nostalgic", "ecstatic", "insane", "cranky", "mad", "jovial", "sick", "hungry", "thirsty", "elegant", "backstabbing", "clever", "trusting", "loving", "suspicious", "berserk", "high", "romantic", "prickly", "evil"]
right = ["albattani", "almeida", "archimedes", "ardinghelli", "babbage", "bardeen", "bartik", "bell", "blackwell", "bohr", "brattain", "brown", "carson", "colden", "curie", "darwin", "davinci", "einstein", "elion", "engelbart", "euclid", "fermat", "fermi", "feynman", "franklin", "galileo", "goldstine", "goodall", "hawking", "heisenberg", "hoover", "hopper", "hypatia", "jones", "kirch", "kowalevski", "lalande", "leakey", "lovelace", "lumiere", "mayer", "mccarthy", "mcclintock", "mclean", "meitner", "mestorf", "morse", "newton", "nobel", "pare", "pasteur", "perlman", "pike", "poincare", "ptolemy", "ritchie", "rosalind", "sammet", "shockley", "sinoussi", "stallman", "tesla", "thompson", "torvalds", "turing", "wilson", "wozniak", "wright", "yonath"]

def get_random_name(sep='_'):
    r = random.SystemRandom()
    return  '%s%s%s' % (r.choice(left), sep, r.choice(right))


class JiraReleaser(object):
	JIRA_ISSUE_REGEX = '[A-Z]+(?!-?[a-zA-Z]{1,10})-\d+'

	def test(self):
		print(self.jira.project_versions(self.project_key)[0].released)

	def create_jira(self, jira_base_url, jira_username, jira_password):
		"""
		"""
		self.jira = JIRA(jira_base_url, basic_auth=(jira_username, jira_password))

	def release_version(self):
		"""
		"""
		version = None
		for project_version in self.jira.project_versions(self.project_key):
			if project_version.name == self.version_name:
				version = project_version

	def list_commits(self):
		"""
		"""
		return list(self.repo.iter_commits('{}..HEAD'.format(self.from_commit)))

	def get_issues(self, commits):
		"""
		"""
		issues = []
		for commit in commits:
			issues.extend(re.findall(self.JIRA_ISSUE_REGEX, commit.message))
		return set(issues)

	def update_issues_version(self, issues):
		"""
		"""
		for issue in issues:
			item = self.jira.issue(issue)
			fixVersions = [{'name': self.version_name}]
			for fix in item.fields.fixVersions:
				fixVersions.append({'name': fix.name})
			item.update(fields={"fixVersions": fixVersions})

	def update_issues_labels(self, issues):
		"""
		"""
		for issue in issues:
			item = self.jira.issue(issue)
			label = self.create_jira_label()
			item.fields.labels.append(label)
			item.update(fields={"labels": issue.fields.labels})

	def create_version_name(self):
		"""
		"""
		versions = set([x.name for x in self.jira.project_versions(self.project_key)])
		version = get_random_name()
		while version in versions:
			version = get_random_name()
		self.version_name = version
		return version

	def create_jira_version(self):
		"""
		"""
		return self.jira.create_version(name=self.create_version_name(),project=self.project_key,releaseDate=str(datetime.now()))

	def create_jira_label(self):
		"""
		"""
		if self.is_development:
			return self.project_name + '-dev-' + self.build_number

	def release_version(self, version):
		version.update(fields={'released': True})

	def __str__(self):
		return 'Project .git: {}\nProject key: {}'.format(self.repo.working_tree_dir, self.project_key)
	def __unicode__(self):
		return u'Project .git: {}\nProject key: {}'.format(self.repo.working_tree_dir, self.project_key)

	def __init__(self, project_key, jira_url, jira_username=None, jira_password=None, project_name=None, from_commit=None, to_commit=None, build_number=None, is_development=False, is_production=False, repo_root=None):
		self.project_key = project_key
		self.from_commit = from_commit
		self.to_commit = to_commit
		self.project_name = project_name
		self.build_number = build_number
		self.is_development = is_development
		self.is_production = is_production
		if not repo_root:
			self.repo = Repo(os.path.dirname(os.path.realpath(__file__)))
		else:
			self.repo = Repo(repo_root)
		self.create_jira(jira_url, jira_username, jira_password)