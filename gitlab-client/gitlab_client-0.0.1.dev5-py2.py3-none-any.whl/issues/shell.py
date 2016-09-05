import gitlab
import ConfigParser, os
from prettytable import PrettyTable

def main():
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.issues.cfg')])
    host = config.get("default", "host")
    token = config.get("default", "token")
    project = config.get("default", "project")
    lab = gitlab.Gitlab(host=host, token=token)
    project = lab.getproject(project)
    table = PrettyTable(["Title","Labels","State"])
    table.align["Title"] = "l"
    table.align["Labels"] = "l"
    
    issues = lab.getprojectissues(project["id"])
    for issue in issues:
        title = issue['title']
        labels = ",".join(issue['labels'])
        state = issue['state']
        table.add_row([title, labels, state])
    
    print(table)
