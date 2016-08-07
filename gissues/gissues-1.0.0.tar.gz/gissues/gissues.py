from .utils import *
from datetime import datetime
import os, subprocess, tempfile
from .app import app

import textwrap

def print_page_header(current_page_number, paginated_list, repo):
    print("== PAGE {} OUT OF {} ==== {} ==".format(current_page_number,
                                                   len(paginated_list),
                                                   repo.full_name))


def display_issue_list(issues):

    issue_entry_str = "<{}>[#{}] {}\n" \
                      "BY: {} [{}]\n" \
                      "COMMENTS: {}\n" \
                      "TAGS: {}\n" \
                      "\n"


    for issue in issues:
        tags = ""
        tags = [tags + "[{}]".format(tag.name) for tag in issue.labels]
        tags = ", ".join(tags)

        print(issue_entry_str.format(issue.state, issue.number,
                                     issue.title,
                                     issue.user.login,
                                     format_date(issue.created_at),
                                     issue.comments,
                                     tags))

def display_issue(issue):
    display_str = "\n\n" + line('=') + "\n<{}>[#{}] {}\n" + "BY: {} [{}]\n"  + line('~') + "\n{}\n" + line('-') + "{} COMMENTS ...\n" + line("=")

    print(display_str.format(issue.state.upper(),
                             issue.number,
                             issue.title,
                             issue.user.login,
                             format_date(issue.created_at),
                             issue.body,
                             issue.comments))



def display_comment_list(comments):
    comment_entry_str = "\n" + line('-') + "[{} commented {}]\n" + "{}\n" + line('-')

    for comment in comments:
        print(comment_entry_str.format(comment.user.login,
                                       format_date(comment.created_at),
                                       comment.body))


def edit_long_text(header="", offset=0):
    text = ""
    editingfile = tempfile.NamedTemporaryFile(mode='w+') #Create Temporary file to edit from

    with editingfile.file as f:
        f.write(header)

        #Makes sure the header is saved to the file.
        #Dont want to close file because the temporary file will be deleted.
        f.flush()
        os.fsync(f.fileno())

        #Put seek pointer at end of file after the header.
        #Everything after the header counts.
        f.seek(0, os.SEEK_END) if offset == 0 else f.seek(offset, os.SEEK_SET)

        p = subprocess.Popen(('nano', editingfile.name))

        #After Text Editor has closed
        p.wait()
        for line in f:
    	       text += line

    return text



def make_new_issue(title):
    print("Creating Issue For: '{}'".format(title))



    file_header = (line('=', 100) +
                   "\t\tEditing Body for Issue:  {}\n".format(title) +
                   "\t\tPLEASE write the body BELOW this header. That is below the line.\n" +
                   "\t\tAnything in this header will now be apart of the issue content\n" +
                   line('=', 100))

    body = edit_long_text(file_header)

    print("Creating Issue...")
    newissue = app.repo.create_issue(title, body)
    print("\n\n **** NEW ISSUE CREATED: [#{}] '{}' @ {}".format(newissue.number, newissue.title ,newissue.html_url))
