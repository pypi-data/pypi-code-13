from slackbot.bot import listen_to
from slackbot import settings


@listen_to('(.*\-\d+)')
def response_issue(message, issue_id=None):
    project = issue_id.split('-')[0]

    if project.upper() not in settings.ALLOWED_PROJECTS:
        return

    issue = settings.jira_class.get_ticket(issue_id)
    if not issue:
        return

    msg = "<%s/browse/%s|%s: %s>\n" % (
        settings.JIRA_SERVER,
        issue_id.upper(),
        issue_id.upper(),
        issue.fields.summary
        )
    msg += "*Created*: %s\n" % issue.fields.created
    msg += "*Priority*: %s\n" % issue.fields.priority
    msg += "*Status*: %s" % issue.fields.status

    message.send_webapi(msg)
