#!/usr/local/bin/python
# encoding: utf-8
"""
*Initialise a deckster presentation with all the required assets*

:Author:
    David Young

:Date Created:
    July 23, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import StringIO
import yaml
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from frankenstein import electric
from commonutils.getpackagepath import getpackagepath


def start(
        log,
        settings,
        destinationPath):
    """Initialise a deckster presentation with all the required assets

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- settings dictionary
        - ``destinationPath`` -- path to the destination folder to initiate the presentation in

    **Return:**
        - None

    **Usage:**

        .. code-block:: python 

            from deckster import start
            start(
                log=log,
                settings=settings,
                destinationPath="/path/to/my/presetnation"
            )
    """
    log.info('starting the ``start`` function')

    projectPath = getpackagepath()
    resourcePath = projectPath + "/resources"

    # ADD REQUIRED SETTINGS FOR FRANKENSTEIN
    newSettings = """
    frankenstein:
        # Add or amend these placeholders
        placeholder delimiters: ["xxx"]
        fixed placeholders:
            # Add your own fixed placeholders. You will not be asked for these values at project creation, but if the placholder keys are used within your template then they will be populated.
            deckster_website: http://www.thespacedoctor.co.uk
    """
    fakeFile = StringIO.StringIO()
    fakeFile.write(newSettings)
    yamlContent = yaml.load(fakeFile.getvalue())
    fakeFile.close()

    if settings:
        if "frankenstein" not in settings:
            settings.update(yamlContent)
    else:
        settings = yamlContent

    # GENERATE THE PRESENTATION SOURCE FROM TEMPLATE
    electric(
        log,
        pathToTemplate=resourcePath,
        pathToDestination=destinationPath,
        settings=settings
    ).get()

    log.info('completed the ``start`` function')
    return None
