from __future__ import print_function

import sys

from slackbot import settings
settings.PLUGINS = [
    'slack_jirer.bot',
    ]
from slackbot.bot import Bot

from .jira_wrapper import JiraWrapper


def main():
    try:
        settings.jira_class = JiraWrapper(
            settings.JIRA_SERVER,
            settings.JIRA_PROJECTS,
            settings.JIRA_USERNAME,
            settings.JIRA_PASSWORD,
            )
        settings.ALLOWED_PROJECTS = settings.JIRA_PROJECTS.split(',')
        settings.ALLOWED_PROJECTS = [project.upper() for project in settings.ALLOWED_PROJECTS]
    except AttributeError:
        print('Missing JIRA_SERVER, JIRA_PROJECTS, JIRA_USERNAME or JIRA_PASSWORD environment variable')
        sys.exit(1)

    print("starting bot...")
    bot = Bot()
    bot.run()
