from __future__ import print_function

import gitlab
import ConfigParser, os
import argparse
from prettytable import PrettyTable


class GitLabShell():

    def __init__(self):
        self.config = {}
        self.gitlab = self.connect()
        
    def connect(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read([os.path.expanduser('~/.gitlab.cfg')])
        host = self.config.get("default", "host")
        token = self.config.get("default", "token")
        return gitlab.Gitlab(host=host, token=token)

    def issues(self):
        projectname = self.config.get("default", "project")
        project = self.gitlab.getproject(projectname)
        table = PrettyTable(["Id", "Title","Labels","State"])
        table.align["Title"] = "l"
        table.align["Labels"] = "l"
        
        issues = self.gitlab.getprojectissues(project["id"])
        for issue in issues:
            id = issue['id']
            title = issue['title']
            labels = ",".join(issue['labels'])
            state = issue['state']
            table.add_row([id, title, labels, state])
        
        print(table)


def main():
    parser = argparse.ArgumentParser(description='Simple GitLab client')
    parser.add_argument('resource', default='repl', nargs='?', help="issues, projects, ...")
    parser.add_argument('--host', type=str)
    parser.add_argument('--username', type=str)
    parser.add_argument('--token', type=str)
    args = parser.parse_args()

    if (args.resource == "issues"):
        GitLabShell().issues()
    if (args.resource == "repl"):
        repl()

def repl():
    print("REPL mode not implemented. Please provide a resource.")
