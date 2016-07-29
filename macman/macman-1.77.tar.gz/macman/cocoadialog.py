#!/usr/bin/python
# Filename: cocoadialog.py

import os
from subprocess import PIPE, Popen
import macman

cocoadialog = '/Applications/CocoaDialog.app/Contents/MacOS/CocoaDialog'

def infoMsgBox(title, informative_text, body_text, button_text='OK'):
    """ Produce an informative, one button message box
    See http://mstratman.github.io/cocoadialog/#standard-inputbox_control for more information
    """

    template = '%s msgbox \
               --title "%s" \
               --no-cancel \
               --string-output \
               --no-newline \
               --informative-text "%s" \
               --float \
               --no-show \
               --text "%s" \
               --button1 "%s" \
               --icon info'

    p = Popen(template % (cocoadialog, title, informative_text, body_text, button_text), shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if output: macman.logs.writeLog('Output: %s' % output)
    if err: macman.logs.writeLog('Error: %s' % err)


def okMsgBox(title, informative_text, body_text):
    """ Produce a Ok/Cancel message box
    See http://mstratman.github.io/cocoadialog/#standard-inputbox_control for more information
    """

    template = '%s ok-msgbox \
               --title "%s" \
               --string-output \
               --informative-text "%s" \
               --float \
               --text "%s" \
               --icon info'

    p = Popen(template % (cocoadialog, title, informative_text, body_text), shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if output: macman.logs.writeLog('Output: %s' % output)
    if err: macman.logs.writeLog('Error: %s' % err)


def dropDownMenu(title, body_text, items):
    """ Produce a two button dropdown menu.
    Dropdown items should be in a space-delimited string or list format

    Will return a list with two values, one indicating the button pushed and one indicating the dropdown value selected

    See http://mstratman.github.io/cocoadialog/#standard-dropdown_control for more information
    """

    # if items in list form, convert to space delimited string
    if isinstance(items, list):
        items = ' '.join(items)

    template = '%s standard-dropdown \
               --title "%s" \
               --text "%s" \
               --float \
               --timeout 120 \
               --string-output \
               --items %s'

    p = Popen(template % (cocoadialog, title, body_text, items), shell=True, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if err: macman.logs.writeLog('Error: %s' % err)

    return output.strip().split()


def notifyBubble(title, body_text, icon='gear'):
        """ Produce a informative message bubble
        See http://mstratman.github.io/cocoadialog/#bubble_control for more information
        """

        if os.path.isfile(icon):
            icon_file = '--icon-file "%s"' % icon
        else:
            icon = 'gear'
            icon_file = '--icon "%s"' % icon

        print icon_file

        template = '%s bubble \
                   --title "%s" \
                   --text "%s" \
                   %s '

        p = Popen(template % (cocoadialog, title, body_text, icon_file), shell=True, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if output: macman.logs.writeLog('Output: %s' % output)
        if err: macman.logs.writeLog('Error: %s' % err)
