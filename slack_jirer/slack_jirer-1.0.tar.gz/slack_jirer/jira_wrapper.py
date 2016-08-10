from jira import JIRA


class JiraWrapper(object):
    def __init__(self, server, user, password, timeout=5.0):
        self.server = server
        self.auth = (user, password)
        self.timeout = timeout

        options = {'server': server}
        self.jira = JIRA(basic_auth=('gitlab', 'zIJo2zQIg38B'), options=options)

    def get_ticket(self, issue_id):
        try:
            return self.jira.issue(issue_id)
        except Exception as e:
            print(e)
            return None
