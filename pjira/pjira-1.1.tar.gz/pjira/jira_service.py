from jira import JIRA as jra
from utils import ConfigManager

class Jira(object):

	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password
		self.jra = jra(host, basic_auth=(user, password))

	@classmethod
	def get_jira_service(cls):
		config_details = ConfigManager.get_details();
		jira = Jira(config_details['host'], config_details['user'], config_details['password'])
		return jira

	def get_issue(self, issue_key):
		issue = self.jra.issue(issue_key)
		return issue

	def create_issue(self, project, title, desc, type ):
		issue_detail = {
			'project': {'key':project},
			'summary': title,
			'description': desc,
			'issuetype':{'name':type}
		}
		return self.jra.create_issue(fields = issue_detail)

	def get_issue_for_user(self, user, project, all):
		user = self.user if user is None else user 
		jql = "assignee = %s" % user
		jql = jql + " and project = %s"%project if project else jql
		jql = jql + " and resolution = Unresolved" if not all else jql
		print jql
		return self.jra.search_issues(jql)

	def add_comment(self, issue_key, comment):
		comment = self.jra.add_comment(issue_key, comment);

class IssueMapper(object):
	def __init__(self, issue):
		self.issue = issue

	def get_short_rep(self):

		return "[%s] - %s" % (self.issue.fields.issuetype, self.issue.fields.summary)

	def get_long_rep(self):
		desc = self.issue.fields.description
		desc = desc.strip() if desc is not None else ""
		return "[Type] - %s\n[Title] - %s\n[Assignee] - %s\t[Reporter] - %s\n[Description]\n%s" % (self.issue.fields.issuetype, self.issue.fields.summary.strip(), self.issue.fields.assignee, self.issue.fields.reporter, desc)