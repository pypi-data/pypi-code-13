from .utils import *
from .gissues import *
from .app import app

import click

import os.path

@click.group()
@click.argument('reponame')
def giss(reponame):
    """CLI to view and manage github issues."""
    #The main gissue command sets up the repo variable for use in sub commands.

    #If the user inputs the owner and name of repo use that
    #otherwise Search for the name in the user's repos
    if '/' in reponame:
        reponame_parts = reponame.split('/')
        app.repo = app.gh.repository(reponame_parts[0], reponame_parts[1])
    else:
        app.repo = app.gh.repository(app.gh.user().login, reponame)




###########################################################################
# VIEW ISSUES
###########################################################################

@giss.command(short_help="Displays a page of issues")
@click.option('-d', '--display', default=10, help="Number of issues to display per page.")
@click.option('-p', '--page', default=1, help="Page number to display.")
@click.option('-s', '--status', default='open', type=click.Choice(['open','closed','all']),help="Display issues that are open, closed, or both")
@click.option('-l', '--label', default='', multiple=True, help="Displays issues with certain label.")
def list(display, page, status, label):


    issues = [issue for issue in app.repo.iter_issues(state=status,
                                                  labels=",".join(label))]

    #Each page is a seperate list of issues.
    issues_paginated = paginate(issues, display)

    #Issues are displayed
    try:
        print_page_header(page, issues_paginated, app.repo)
        display_issue_list(issues_paginated[page-1])
        print_page_header(page, issues_paginated, app.repo)
    except IndexError:
        print("ERROR:  Page Not Found: {}".format(page))


@giss.command(short_help="Show content of an issue")
@click.argument('issuenumber')
def show(issuenumber):
    issue = app.repo.issue(issuenumber)

    if issue is None:
        print("ERROR: Issue #{} not found".format(issuenumber))
        return

    display_issue(issue)



###########################################################################
# MANAGE ISSUES
###########################################################################

@giss.command(short_help="Create a new issue")
@click.option('-t', '--issuetitle', required=True, prompt="Type in a TITLE for issue", help="Title of the new issue.")
def make(issuetitle):#######
    make_new_issue(issuetitle)

@giss.command(short_help="Edit an issue")
@click.argument('issuenumber')
@click.option('-t', '--issuetitle', is_flag=True, help="")
def edit(issuenumber, issuetitle):
    issue = app.repo.issue(issuenumber)

    if issue is None:
        print("ERROR: Issue #{} not found".format(issuenumber))
        return

    title = issue.title

    if issuetitle:
        print("Setting NEW title for [#{}] '{}'".format(issue.number, issue.title))
        title = input("New Title: ")

    print("Now editing body for [#{}] '{}'...".format(issue.number, issue.title))

    file_header = (line('=', 100) +
                   "\t\tEditing Body for Issue:  {}\n".format(title) +
                   "\t\tPLEASE write the body BELOW this header. That is below the line.\n" +
                   "\t\tAnything in this header will now be apart of the issue content\n" +
                   line('=', 100))
    old_body = issue.body
    new_body = edit_long_text(file_header+old_body, len(file_header))

    if old_body == new_body:
        print("No changes made to [#{}] '{}'".format(issue.number, issue.title))
        return

    issue.edit(title=title, body=new_body)
    print(" **** Issue [#{}] '{} has been EDITED @ {}".format(issue.number, issue.title, issue.html_url))


@giss.command(short_help="Create/View an issue comment")
@click.argument('issuenumber')
@click.option('-s', '--show', is_flag=True, help="")
@click.option('-p', '--page', default=1, help="")
def comment(issuenumber, show, page):

    issue = app.repo.issue(issuenumber)

    if issue is None:
        print("ERROR: Issue #{} not found".format(issuenumber))
        return

    #If the show option is toggled show the comments
    if show:
        comments = [comment for comment in issue.iter_comments()]
        comments_paginated = paginate(comments, 5)


        print_page_header(page, comments_paginated, app.repo)
        display_comment_list(comments_paginated[page-1])
        print_page_header(page, comments_paginated, app.repo)

    #If not then create a new comment
    else:
        issue = app.repo.issue(issuenumber)
        print("Now creating comment on issue [#{}] '{}'...".format(issue.number, issue.title))

        file_header = (line('=', 100) +
                       "\t\tEditing Body for Comment on Issue:  '{}'\n".format(issue.title) +
                       "\t\tPLEASE write the body BELOW this header. That is below the line.\n" +
                       "\t\tAnything in this header will now be apart of the comment content\n" +
                       "\n\n" +
                       "\t\t[#{}] {} BY {}\n\n".format(issue.number, issue.title, issue.user.login) +
                       issue.body +
                       line('=', 100))

        comment_body = edit_long_text(file_header)

        #Do NOT send an empty comment.
        if not comment_body == "":
            issue.create_comment(comment_body)
        else:
            print(" ERR: Comment Body Empty")
            print(" Comment creation FAILED.\n")
            return

        print(" **** Comment Successfully CREATED for [#{}] '{}'...".format(issue.number, issue.title))


@giss.command(short_help="Reopen a closed issue")
@click.argument('issuenumber')
@click.option('-y', '--yes', is_flag=True, help="")
def open(issuenumber, yes):

    issue = app.repo.issue(issuenumber)

    if issue is None:
        print("ERROR: Issue #{} not found".format(issuenumber))
        return

    #Confirm if user wants to reopen the issue.
    if not yes:
        if not confirm("open"): return


    print("*** Reopening issue number [#{}]...".format(issuenumber))
    #Opens issue
    issue.reopen()
    print("*** Issue [#{}] is now OPEN".format(issuenumber))


@giss.command(short_help="Close an issue")
@click.argument('issuenumber')
@click.option('-y', '--yes', is_flag=True, help="")
def close(issuenumber, yes):
    issue = app.repo.issue(issuenumber)

    if issue is None:
        print("ERROR: Issue #{} not found".format(issuenumber))
        return

    if not yes:
        if not confirm("close"): return

    print("*** Closing issue number [#{}]...".format(issuenumber))
    #Closes Issue
    issue.close()
    print("*** Issue [#{}] is now CLOSED".format(issuenumber))


#################################################################################
#################################################################################


if __name__ == '__main__':
    giss()
