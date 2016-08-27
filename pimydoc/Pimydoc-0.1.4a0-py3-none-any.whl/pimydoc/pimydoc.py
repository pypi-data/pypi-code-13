#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Pimydoc Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Pimydoc.
#    Pimydoc is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pimydoc is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pimydoc.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Pimydoc by suizokukan (suizokukan @t orange d@t fr)

    Pimydoc : [P]lease [i]nsert my doc[umentation]

    A Python3/GPLv3/OSX-Linux-Windows/CLI project, using no additional modules
    than the ones installed with Python3.
    ____________________________________________________________________________

    Pimydoc inserts in source files the text paragraphs stored in "pimydoc", the
    documentation source file. Moreover, the script updates the text paragraphs
    already present in the source files if the documentation source file has
    changed.
    ____________________________________________________________________________

    usage : $ pimydoc.py      : modify the current directory with a "pimydoc"
                                file in the current directory.

    try pimydoc --help for more options and see README.md for more documentation.
"""

import argparse
import logging
import os
import re
import shutil
import sys

#///////////////////////////////////////////////////////////////////////////////
def remove_and_return_linefeed(src):
    """
        remove_and_return_linefeed()
        ________________________________________________________________________

        Remove the linefeed characters from the end of (str)src.
        This function recognizes three kinds of linefeed characters :
        o the Linux one (\n)
        o the Windows one (\r\n)
        o the ancient OSX one (\r)
        ________________________________________________________________________

        PARAMETER : (str)src, the source string to be cut

        RETURNED VALUE : ((str)the reduced source string,
                          (str)the linefeed characters)
    """
    if src.endswith("\r\n"):
        return src[:-2], "\r\n"
    elif src.endswith("\n"):
        return src[:-1], "\n"
    elif src.endswith("\r"):
        return src[:-1], "\r"
    else:
        return src

#///////////////////////////////////////////////////////////////////////////////
def normpath(_path):
    """
        normpath()
        ________________________________________________________________________

        Return a human-readable (e.g. "~" -> "/home/myhome/" on Linux systems),
        normalized version of a path.
        ________________________________________________________________________

        PARAMETER : (str)_path

        RETURNED VALUE : the expected string
    """
    res = os.path.normpath(os.path.abspath(os.path.expanduser(_path)))

    if res == ".":
        res = os.getcwd()

    return res

#===============================================================================
# project's settings
#
# • for __version__ format string, see https://www.python.org/dev/peps/pep-0440/ :
#   e.g. "0.1.2.dev1" or "0.1a"
#
# • See also https://pypi.python.org/pypi?%3Aaction=list_classifiers
#
#===============================================================================
PROJECT_NAME = "Pimydoc"

# see https://www.python.org/dev/peps/pep-0440/
# e.g. 0.1.2.dev1, 0.0.6a0
PROJECT_VERSION = "0.1.4a"

# constants required by Pypi.
__projectname__ = PROJECT_NAME
__author__ = "Xavier Faure (suizokukan)"
__copyright__ = "Copyright 2016, suizokukan"
__license__ = "GPL-3.0"
__licensepypi__ = 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
__version__ = PROJECT_VERSION
__maintainer__ = "Xavier Faure (suizokukan)"
__email__ = "suizokukan @T orange D@T fr"
__status__ = "Alpha"
__statuspypi__ = 'Development Status :: 3 - Alpha'

################################################################################
class Settings(dict):
    """
        Settings class
        ________________________________________________________________________

        Use this class to store the settings used by the pimydoc_a_file()
        function.
        The settings are stored as in a dictionary : (str)key->(str)value

        REGEX_SOURCE_FILTER : regex describing the name of the files to be
                              modified.

        REGEX_FIND_DOCTITLE : regex describing the name (in the documentation
                              source file) of the titles.
                              See below for more details (docsrc format)

        STARTSYMB_IN_DOC    : string at the beginning of each line of
                              documentation added in the source files.
                              See below for more details (docsrc format)

        STARTSYMB_IN_DOC__ESCAPE : re.escape(STARTSYMB_IN_DOC)

        REGEX_FIND_PIMYDOCLINE_IN_CODE : string at the beginning of each line of
                                         documentation added in the source files.

        REGEX_FIND_PIMYDOCLINE_IN_CODE2: same as REGEX_FIND_PIMYDOCLINE_IN_CODE
                                         but without final spaces.

        PROFILE_PYTHON_SPACENBR_FOR_A_TAB : (int) for Python files, number of
                                            spaces replacing a tab character.

        REMOVE_FINAL_SPACES_IN_NEW_DOCLINES : (str) "True" or "False"
        ________________________________________________________________________
        about the docsrc format :
        | | This text has been automatically added by Pimydoc.
        | | expliquer que on peut laisser un espace après STARTSYMB_IN_DOC
        | |
        | | Le fichier pimydoc est précis :
        | | 	STARTSYMB_IN_DOC :|_|_
        | | ne donnera pas le même résultat que :
        | | 	STARTSYMB_IN_DOC :|_|
        | |
        | | La raison d'être de "REGEX_FIND_PIMYDOCLINE_IN_CODE2" est qu'avec
        | | REGEX_FIND_PIMYDOCLINE_IN_CODE on attrape des lignes telles que :
        | | ____| |_doc
        | | ____| |_doc_
        | | ____| |_doc
        | | mais pas de lignes comme :
        | | ____| |
        | | ...car le dernier espace a été supprimé grâce à REMOVE_FINAL_SPACES_IN_NEW_DOCLINES .
        | |
        ________________________________________________________________________

        class attributes : -

        instance attribute(s) : -

        class methods :
            • __init__(self)
            • init_from_line(self, line)

        todo : documenter le jeu des re.escape()
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            Settings.__init__()
            ________________________________________________________________________

            Initialize all the settings to a default value.
            ________________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        dict.__init__(self)

        # this is a direct initialization : see the .init_from_line() method to
        # see how self can be initialized from a file.
        self["REGEX_SOURCE_FILTER"] = ""
        self["REGEX_FIND_DOCTITLE"] = "^\\[(?P<name>.+)\\]$"
        self["STARTSYMB_IN_DOC"] = "| | "
        self["STARTSYMB_IN_DOC__ESCAPE"] = re.escape(self["STARTSYMB_IN_DOC"])
        self["REGEX_FIND_PIMYDOCLINE_IN_CODE"] = "^\\s*" + self["STARTSYMB_IN_DOC"]
        self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"] = "^\\s*" + self["STARTSYMB_IN_DOC"]
        self["PROFILE_PYTHON_SPACENBR_FOR_A_TAB"] = 4
        self["REMOVE_FINAL_SPACES_IN_NEW_DOCLINES"] = "True"

    #///////////////////////////////////////////////////////////////////////////
    def init_from_line(self, line):
        """
            Settings.init_from_line()

            returned value : 0 if success, -1 if an important problem occured
        """
        returned_value = 0

        key, value = line.split(":")
        key = key.strip()

        value, _ = remove_and_return_linefeed(value)
        logging.debug("read a new setting : key='%s', value='%s'", key, value)

        if key not in self:
            logging.error("! unknown key '%s'.", key)
            returned_value = -1
        else:
            try:
                if key == "REGEX_FIND_DOCTITLE":
                    self[key] = re.compile(value.lstrip())
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "REGEX_SOURCE_FILTER":
                    self[key] = re.compile(value.lstrip())
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "STARTSYMB_IN_DOC":
                    self[key] = value
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                    self["STARTSYMB_IN_DOC__ESCAPE"] = re.escape(self["STARTSYMB_IN_DOC"])
                    logging.debug("key 'STARTSYMB_IN_DOC__ESCAPE' set to '%s' (%s).",
                                  self["STARTSYMB_IN_DOC__ESCAPE"], type(self[key]))

                elif key == "REGEX_FIND_PIMYDOCLINE_IN_CODE":
                    value = value.replace("STARTSYMB_IN_DOC", SETTINGS["STARTSYMB_IN_DOC__ESCAPE"])
                    self[key] = value.lstrip()

                    self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"] =\
                        self["REGEX_FIND_PIMYDOCLINE_IN_CODE"][:]
                    while self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"].endswith("\\ "):
                        self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"] = \
                            self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"][:-2]

                    self["REGEX_FIND_PIMYDOCLINE_IN_CODE"] = \
                        re.compile(self["REGEX_FIND_PIMYDOCLINE_IN_CODE"])
                    self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"] = \
                        re.compile(self["REGEX_FIND_PIMYDOCLINE_IN_CODE2"])

                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "PROFILE_PYTHON_SPACENBR_FOR_A_TAB":
                    self[key] = int(value)
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "REMOVE_FINAL_SPACES_IN_NEW_DOCLINES":
                    self[key] = value.strip()
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                else:
                    logging.error("! unknown setting key : '%s' (set to '%s')", key, self[key])

            except re.error as error:
                logging.error("! A regex error occured by reading the following line :")
                logging.error(line)
                logging.error("! The key to be read was '%s'", key)
                logging.error("! Error message returned by the script : '%s'", error)
                returned_value = -1

        return returned_value

SETTINGS = Settings()

################################################################################
class CommandLineParser(argparse.ArgumentParser):
    """
        CommandLineParser class
        ________________________________________________________________________

        Use this class to parse the command line arguments.

        Unique instance : args (see at the end of the file)
        ________________________________________________________________________

        class attributes :

            • (str)description
            • (str)epilog

        instance attribute(s) : -

        class methods :

            • __init__()
            • get_args()
    """
    description = "{0} project, v.{1}".format(PROJECT_NAME,
                                              PROJECT_VERSION)

    epilog = "{0}'s author : " \
             "suizokukan (suizokukan _A.T_ orange DOT fr)".format(PROJECT_NAME)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
                CommandLineParser.__init__()
                ________________________________________________________________

                Initialize the object by adding all the arguments.
                ________________________________________________________________

                PARAMETERS      : no parameter

                RETURNED VALUE    : no RETURNED VALUE
        """
        argparse.ArgumentParser.__init__(self,
                                         description=CommandLineParser.description,
                                         epilog=CommandLineParser.epilog,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        self.add_argument('--sourcepath',
                          type=str,
                          default=normpath(os.getcwd()),
                          help="source path of the code")

        self.add_argument("--docsrcfile",
                          type=str,
                          default=normpath(os.path.join(os.getcwd(), "pimydoc")),
                          help="source documentation file name")

        self.add_argument('--verbose',
                          type=int,
                          choices=(0, 1, 2),
                          default=1,
                          help="degree of verbosity of the output. " \
                               "0 : only the error messages; " \
                               "1 : all messages except debug messages; " \
                               "2 : all messages, including debug messages; " \
                               "See also the -vv and -vvv options.")

        self.add_argument('-vv',
                          action='store_true',
                          help="verbosity set to 1 (all messages except debug messages).")

        self.add_argument('-vvv',
                          action='store_true',
                          help="verbosity set to 2 (all messages, including debug messages).")

        self.add_argument('--version', '-v',
                          action='version',
                          version="{0} v. {1}".format(__projectname__, __version__),
                          help="show the version and exit")

        self.add_argument('--remove', '-r',
                          action='store_true',
                          help="Remove every pimydoc line in all the files of the source directory")

        self.add_argument('--securitymode', '-s',
                          action='store_true',
                          help="Security mode : backup files created by Pimdoc are not deleted")

    #///////////////////////////////////////////////////////////////////////////
    def get_args(self):
        """
                CommandLineParser.get_args()
                ________________________________________________________________

                Parse the command line arguments and return the argparse.Namespace
                object.
                ________________________________________________________________

                PARAMETER(S)    : no parameter

                RETURNED VALUE    : the argparse.Namespace object
        """
        return self.parse_args()

################################################################################
class DocumentationSource(dict):
    """
        DocumentationSource class
        ________________________________________________________________________

        self.errors = [] a list of str
        ________________________________________________________________________
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, filename):
        """
            Initialize self and SETTINGS from the content of filename.
        """

        def newline(line, linenumber, location, current_title):
            """
                newline() :  a subfunction of DocumentationSource.__init__()
                ________________________________________________________________

                Add the line to the settings or the current doc title.
                ________________________________________________________________

                ARGUMENTS :
                • line          : (str) line to be added
                • linenumber    : (int) line number in the source file
                • location      : (str) see __init__() : None, "doc", ...
                • current_title : (str) the current doc title.

                RETURNED VALUE : ((str)location, (str)current_title, (bool)stop)
            """
            stop = False

            find_title = re.search(SETTINGS["REGEX_FIND_DOCTITLE"], line)

            if find_title is not None:
                location = "doc"
                logging.debug("beginning of the doc at line '%s' (#%s)",
                              line.strip(), linenumber)

            if location == "settings":
                separator = line.find(":")

                if separator >= 0:
                    if SETTINGS.init_from_line(line) != 0:
                        logging.error("! An error occured : " \
                                      "stop reading the documentation source file.")
                        self.errors.append("Can't read the " \
                                           "line '{0}' (#{1})".format(line, linenumber))
                        stop = True
                elif len(line.strip()) > 0:
                    logging.error("! (reading the documentation source file) " \
                                  " Can't read the following line : '%s' (#%s)",
                                  line, linenumber)

            elif location == "doc":

                if find_title is None:
                    self[current_title].append(line)
                else:
                    try:
                        new_title = find_title.group("doctitle")
                    except IndexError as error:
                        logging.error("! An error occured : " \
                                      "stop reading the documentation source file.")
                        self.errors.append("Can't read the line '{0}' (#{1}) : " \
                                           "ill-formed doctitle".format(line, linenumber))
                        self.errors.append("Error returned by Python :"+str(error))
                        stop = True

                    if new_title in self:
                        logging.error("! title '%s' already defined !", new_title)
                    self[new_title] = []
                    current_title = new_title

                    logging.debug("found a new title : '%s' (#%s)", new_title, linenumber)

            return location, current_title, stop

        # ---------------------------------------------
        # entry point of DocumentationSource.__init__()
        logging.debug("DocumentationSource.__init__() : %s", filename)

        # a list of (str)
        self.errors = []

        if not os.path.exists(filename):
            logging.error("! Missing documentation source file '%s'", filename)
            self.errors.append("Can't open '%s'", filename)
            return

        # title(str) : a list of str
        dict.__init__(self)

        # None or the current (str)doc title
        current_title = None

        # None is mandatory if a blank line appears before the first title
        location = None # None / settings / doc

        with open(filename) as src:
            stop = False
            for linenumber, line in enumerate(src.readlines()):

                if line.startswith("###"):
                    logging.debug("Skipped commentary line '%s'", line.strip())
                elif line.strip() == "[pimydoc]":
                    location = "settings"
                    logging.debug("settings detected by reading the '%s' line (#%s).",
                                  line.strip(), linenumber)
                else:
                    location, current_title, stop = newline(line, linenumber,
                                                            location, current_title)

                if stop:
                    break

#///////////////////////////////////////////////////////////////////////////////
def pimydoc_a_file(targetfile_name, docsrc, just_remove_pimydoc_lines, securitymode):
    """
        Update the documentation in a file.
        ________________________________________________________________________

        Read a target file, removed the old documentation and replace it by the
        new one described in <docsrc>.
        ________________________________________________________________________

        ARGUMENTS :
        • targetfile_name           : name of the file to be modified
        • docsrc                    : a DocumentationSource object
        • just_remove_pimydoc_lines : if True, nothing is added but the pimydoc
                                      lines of documentation are removed.
        • securitymode              : (bool) True if the backup files created
                                      by this function have to be kept.

        no RETURNED VALUE
    """

    def rewrite_new_targetfile(targetfile_name, just_remove_pimydoc_lines):
        """
            rewrite_new_targetfile() : this function is a part of the pimydoc_a_file()
            function.
            ________________________________________________________________________

            Rewrite the target file with the documentation to be added.
            ________________________________________________________________________

            ARGUMENTS :
            • targetfile_name           : name of the file to be modified
            • just_remove_pimydoc_lines : if True, nothing is added but the pimydoc
                                          lines of documentation are removed.

            no RETURNED VALUE
        """
        with open(targetfile_name, "w") as newtargetfile:
            for linenumber, line in enumerate(targetcontent):

                if re.search(SETTINGS["REGEX_FIND_PIMYDOCLINE_IN_CODE"], line) is None and \
                   re.search(SETTINGS["REGEX_FIND_PIMYDOCLINE_IN_CODE2"], line) is None:
                    newtargetfile.write(line)

                if linenumber in lines_with_trigger:
                    # let's add the expected documentation :
                    doc_content = docsrc[lines_with_trigger[linenumber]]
                    doc_title = lines_with_trigger[linenumber]

                    if just_remove_pimydoc_lines is False:
                        logging.info("+ adding some doc in '%s'; doctitle='%s'",
                                     targetfile_name, doc_title)

                        if profile == "Python":
                            _line = line.replace("\t",
                                                 " "*SETTINGS["PROFILE_PYTHON_SPACENBR_FOR_A_TAB"])
                            spacenumber = _line.find(doc_title)
                        else:
                            spacenumber = line.find(doc_title)

                        for docline in doc_content:
                            new_docline = " "*spacenumber+SETTINGS["STARTSYMB_IN_DOC"]+docline
                            if SETTINGS["REMOVE_FINAL_SPACES_IN_NEW_DOCLINES"] == "True":
                                new_docline, new_doclinefeed = \
                                    remove_and_return_linefeed(new_docline)
                                new_docline = new_docline.rstrip()
                                new_docline += new_doclinefeed
                            newtargetfile.write(new_docline)

    # ----------------------------
    # here begins pimydoc_a_file()
    logging.debug("- - pimydoc_a_file() : %s", targetfile_name)

    # --------------------------------------
    # choose a profile for the target file :
    profile = None
    if targetfile_name.endswith(".py"):
        profile = "Python"
    elif targetfile_name.endswith(".cpp") or targetfile_name.endswith(".h"):
        profile = "C++"
    logging.debug("for %s, the profile '%s' will be used.", targetfile_name, profile)

    # -------------------------------------------
    # let's read the content of the target file :
    try:
        targetcontent = open(targetfile_name).readlines()
    except FileNotFoundError as error:
        logging.error("! Can't read the content of the file '%s'", targetfile_name)
        logging.error("! Error returned by Python : "+str(error))
        logging.error("! Skipping this file.")
        return

    # ---------------------------
    # fill <lines_with_trigger> :

    # (int)line number : (str)name of the doc title to be added after the line
    lines_with_trigger = dict()

    for linenumber, line in enumerate(targetcontent):
        for doctitle in docsrc:
            if doctitle in line:
                lines_with_trigger[linenumber] = doctitle

    # -------------
    # backup file :
    shutil.copy(targetfile_name, targetfile_name+"_pimydoc_backup")

    # --------------------------
    # delete (old) target file :
    os.remove(targetfile_name)

    # ------------------------------------------------
    # rewrite (new) target file with the new content :
    rewrite_new_targetfile(targetfile_name, just_remove_pimydoc_lines)

    # -------------------------------------------------------------------
    # give to the new target file the permission of the old target file :
    shutil.copystat(targetfile_name+"_pimydoc_backup", targetfile_name)

    # --------------------
    # remove backup file :
    if securitymode is False:
        os.remove(targetfile_name+"_pimydoc_backup")

    logging.debug("--- done with %s", targetfile_name)

#///////////////////////////////////////////////////////////////////////////////
def pimydoc(args, just_remove_pimydoc_lines, docsrc):
    """
        pimydoc() function
        ____________________________________________________________________

        to be called from another script after args  has been filled : this
        function doesn't read the arguments on the command line.
        ____________________________________________________________________

        no ARGUMENT, no RETURNED VALUE
    """

    number_of_files = 0
    number_of_discarded_files = 0

    for dirpath, _, filenames in os.walk(normpath(args.sourcepath)):
        for filename in filenames:
            number_of_files += 1
            fullname = os.path.join(normpath(dirpath), filename)

            if re.search(SETTINGS["REGEX_SOURCE_FILTER"], fullname):
                if fullname == args.docsrcfile:
                    logging.info("- discarded the documentation source file '%s'", fullname)
                    number_of_discarded_files += 1
                else:
                    pimydoc_a_file(fullname, docsrc,
                                   just_remove_pimydoc_lines, args.securitymode)
            else:
                number_of_discarded_files += 1
                if args.vvv is True or args.verbose == 2:
                    logging.info("- discarded '%s'", fullname)

    logging.info("Read %s files, modified %s files, discarded %s files.",
                 number_of_files,
                 number_of_files - number_of_discarded_files,
                 number_of_discarded_files)

#///////////////////////////////////////////////////////////////////////////////
def main():
    """
        main()
        ________________________________________________________________________

        Main entry point. Fill the args variable. Launch the pimydoc()
        function.

        exit codes
        | |  0 if success
        | | -1 if the documentation source file doesn't exist
        | | -2 if the documentation source file is ill-formed
        ________________________________________________________________________

        no PARAMETER

        no RETURNED VALUE
    """
    args = CommandLineParser().get_args()

    if args.vv:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    elif args.vvv:
        logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)
    elif args.verbose == 0:
        logging.basicConfig(format="%(message)s", level=logging.ERROR)
    elif args.verbose == 1:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    elif args.verbose == 2:
        logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)

    logging.info("=== pimydoc : entry point ===")
    logging.debug("main() : args.docsrcfile='%s'; args.sourcepath='%s'",
                  args.docsrcfile, args.sourcepath)

    if args.securitymode:
        logging.info("Security mode activated : " \
                     "the backup files created by the program will not be deleted.")

    if not os.path.exists(args.docsrcfile):
        logging.error("! The expected documentation source file '%s' doesn't exist.",
                      args.docsrcfile)
        logging.error("=== leaving pimydoc ===")
        sys.exit(-1)

    docsrc = DocumentationSource(args.docsrcfile)

    if len(docsrc.errors) > 0:
        logging.error("! Errors occured by reading the documentation source file :")
        for err_msg in docsrc.errors:
            logging.error(err_msg)
            logging.error("=== leaving pimydoc ===")
            sys.exit(-2)

    just_remove_pimydoc_lines = False
    if args.remove:
        logging.info("Let's remove every pimydoc line from the source directory.")
        just_remove_pimydoc_lines = True

    pimydoc(args, just_remove_pimydoc_lines, docsrc)

    logging.info("=== pimydoc : exit point ===")

    sys.exit(0)

#///////////////////////////////////////////////////////////////////////////////
#/////////////////////////////// STARTING POINT ////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()
