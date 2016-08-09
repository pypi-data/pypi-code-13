# coding=utf-8
""" This module provide a easy, non intrusive way to process a big list of files
in a parallel way. Also provides the option to process theses files with a
different packs of options, evaluate and generate reports.

= Requirements:

You need the PPSS script in same dir of this file.

= Instructions:

1. Import this module from your main file
 import pycorpus

2. Create the function that process the file

 def my_process(file_name, config):
     # Do some science stuff with the file

3. (Optional) Create a function that return a argument parser that capture all
the configs that you need.

 def my_parser():
    # Set up your argparse parser
    # Return the parser
    return my_parser_instance

4. Add to the end of your file something like this:

 if __name__ == "__main__":
    corpus_processor = pycorpus.CorpusProcessor(
        parse_cmd_arguments=my_parser, process_file=my_process)
    corpus_processor.run_corpus()

= NOTES:

 * Dot not ADD the () to my_parser and my_process arguments.

 * If you don't need options you can ignore step 3 and the config file come as
 None. But never use the --config parameter.

 * The files are processed in a concurrent way so if you might store any results
  don't use the sys.out use a file.


This module uses PPSS(Louwrentius(c)) that is under GPL licence for further
information see inside PPSS script.
"""

import os
import sys
import re
import argparse
import subprocess
import tempfile
import shutil
import smtplib
from logging import getLogger

__author__ = 'Josu Bermúdez <josu.bermudez@deusto.es>'
__created__ = '06/2013'

logger = getLogger("pycorpus")


class CorpusProcessor:
    """ The class that manages the parallel process of all files of the corpus.
    Also have useful functions like send_mail and launch.
    """
    separator = ":"

    @classmethod
    def launch(cls, command, cwd=None):
        """Launch a process send the input and return the error an out streams.
        :param cwd: The working directory (optional).
        :param command: The command to launch
        """
        err = ""
        try:
            p = subprocess.Popen(command, stderr=subprocess.PIPE, cwd=cwd)
            p.wait()
            err = p.stderr.read()
        except Exception as ex:
            logger.error("Error running {0}:\n{1}".format(command, ex))

        return err

    @classmethod
    def launch_with_output(cls, command, cwd=None):
        """Launch a process send the input and return the error an out streams.
        :param cwd: The working directory (optional).
        :param command: The command to launch

        """
        p = subprocess.Popen(
            command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
        out, err = p.communicate()
        return err, out

    def process_files(self, file_list, config, common, jobs=None):
        """Call a process that executes process function over selected files
        with the config argument

        :param jobs: The maximun number of concurrent jobs
        :param common:  Common configuration to all experiments
        :param file_list: The list of files to process.
        :param config: The config file to process the file
        """
        logger.info("Corpus of {0} started".format(len(file_list)))
        path_here = os.path.dirname(__file__)
        main_name = sys.modules['__main__'].__file__
        main_path = os.path.dirname(main_name)
        work_dir = os.getcwd()
        ppss_work_dir = os.path.join(os.getcwd(), "ppss_dir")

        logger.debug("Script Working directory:{0}".format(ppss_work_dir))
        logger.debug("Working directory:{0}".format(work_dir))
        logger.debug("Main directory:{0}".format(main_path))
        logger.debug("Script directory:{0}".format(path_here))

        # Clean the PPSS working directory
        self.clean_ppss_dir(ppss_work_dir)
        # Slice the work and launch ppss
        size = len(file_list)
        slot = 500
        # In case of not enough for a full slot a support index
        index = -1
        for index in range(size/slot):
            slot_start = index * slot
            slot_end = (index + 1) * slot
            file_slice = file_list[slot_start:slot_end]
            self.process_slot(common, config, file_slice, jobs, main_name, path_here, work_dir)
            self.store_log(ppss_work_dir, work_dir)
            self.clean_ppss_dir(ppss_work_dir)
        # The part that not complete a slot
        rest = size % slot
        if rest:

            slot_start = (index + 1) * slot
            slot_end = slot_start + rest
            file_slice = file_list[slot_start:slot_end]
            self.process_slot(common, config, file_slice, jobs, main_name, path_here, work_dir)
            self.store_log(ppss_work_dir, work_dir)
            self.clean_ppss_dir(ppss_work_dir)
        logger.info("Corpus Processed")

    @staticmethod
    def clean_ppss_dir(ppss_work_dir):
        if os.path.exists(ppss_work_dir):
            shutil.rmtree(ppss_work_dir)
            pass

    @staticmethod
    def store_log(ppss_work_dir, work_dir):
        log_path = os.path.join(work_dir, "log_ppss")
        logger.debug("Target log path: %s", log_path)
        ppss_log_path = os.path.join(ppss_work_dir, "job_log")
        logger.debug("Original log path: %s", ppss_log_path)
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        for root, dirs, files in os.walk(ppss_log_path):
            # In case of no recursive adding
            for fullname in files:
                logger.debug("Log file log path: %s", os.path.join(root, fullname))
                shutil.copy(os.path.join(root, fullname), log_path)

    def process_slot(self, common, config, file_list, jobs, main_name, path_here, work_dir):
        # Prepare and launch PPSS
        with tempfile.NamedTemporaryFile("w", delete=False) as file_list_temp_file:
            logger.debug("Temp File:{0}".format(file_list_temp_file.name))
            # Create a temp file with the files
            file_list_temp_file.write("\n".join(file_list) + "\n")
            file_list_temp_file.close()
            # Create the command that PPSS is going to launch
            command = \
                'python  {0} --thread --thread_file "$ITEM"'.format(main_name)
            if config:
                command += ' --thread_config {0}'.format(config)
                if common:
                    command += self.separator + common
            # Create the PPSS full command
            ppss_command = [path_here + "/ppss", "-f", file_list_temp_file.name,
                            "-c", command]
            if jobs:
                ppss_command.extend(("-p", jobs))
            # Launch
            err = self.launch(ppss_command, cwd=work_dir)
            err = re.sub(r"sed: -e[^\n]*\n", "", err)
            # Print if Errors
            if err:
                logger.error(err)
            # Remove temp file
            os.remove(file_list_temp_file.name)

    @staticmethod
    def _create_file_list(options):
        """ With the argument create a unique file list that contains all files
        that must be processed.

        :param options: Namespace with options(from argsparse). Usable options:

            +files: Files processed(if a directory is provided these are added
                anyway)
            +directories: All the files contained by the directory(recursively)
                are processed.
            +extension:The extensions of the files(without pint) that must be
                processed form directories. The '*' and '*.*' are accepted as
                all extensions. WARNING doesn't filter files from --files.
        """
        # Generate unique file list
        no_filter_extensions = "*" in options.extensions
        # Add the selected files
        file_list = options.files or []
        # Add the files included in the directories
        for directory in options.directories:
            for root, dirs, files in os.walk(os.path.expanduser(directory)):
                # In case of no recursive adding
                for fullname in files:
                    name, ext = os.path.splitext(fullname)
                    # Remove staring point
                    if len(ext) and ext[0] == ".":
                        ext = ext[1:]
                    # Filter , if necessary, the included files
                    if no_filter_extensions or (ext in options.extensions):
                        file_list.append(
                            os.path.abspath(os.path.join(root, fullname)))
        return file_list

    @staticmethod
    def parse_cmd_arguments():
        """ Parse command line arguments and put options into a object.
        """
        parser = argparse.ArgumentParser(description="Process a text file or a \
            directory tree of files using multriprocess",
                                         fromfile_prefix_chars="@")
        parser.add_argument(
            '--jobs', dest='jobs', action='store', default=None,
            help="Set the max number of parallel process")

        parser.add_argument(
            '--files', dest="files",  nargs='*', action='store', default=[],
            help="Files processed(if a directory is specified these "
                 "are added to the list).")
        parser.add_argument(
            '--directories', dest='directories', nargs='*', action="store",
            default=[],
            help="All the files contained by the directory(recursively) "
                 "are processed.")
        parser.add_argument(
            '--extension', nargs='*', dest='extensions', action='store',
            default=('txt',),
            help="The extensions of the files(without dot) that must "
                 "be processed form directories."
                 "The '*' is the expression used as accept all."
                 "WARNING doesn't filter files from --files.")
        parser.add_argument(
            '--config', nargs='*', dest='config', action='store', default=None,
            help="The config files that contains the parameter for threads."
                 "May be multiple files separated by '{0}'. One file per "
                 "experiment unit combinations"
            .format(CorpusProcessor.separator))
        parser.add_argument(
            '--common', dest='common', action='store', default=None,
            help="A common config for all parameters."
                 "May be multiple files separated by '{0}'"
            .format(CorpusProcessor.separator))

        parser.add_argument(
            '--evaluate', dest='evaluate', action='store_true',
            help="Activates the evaluation.")
        parser.add_argument(
            '--report', dest='report', action='store_true',
            help="Activates report system.")
        # Thread parameters
        parser.add_argument(
            '--thread', dest='thread', action='store_true',
            help="NEVER EVER USE!")
        parser.add_argument(
            '--thread_file', dest="thread_file", action='store', default=None,
            help="NEVER EVER USE!")
        parser.add_argument(
            '--thread_config', dest="thread_config", action='store',
            default=None,
            help="NEVER EVER USE!")
        return parser

    def __init__(self, generate_parser_function, process_file_function,
                 evaluation_script=None, report_script=None):
        self.parser_generator = generate_parser_function
        self.process_file_function = process_file_function
        self.evaluation_script = evaluation_script
        self.report_script = report_script
        self.arguments = None

    def rebuild_tread_parameter(self, thread_config, common, process_parser):
        args = []
        if common:
            thread_config += self.separator + common
        for arg_file in thread_config.split(self.separator):
            args.extend(open(arg_file, "r").read().split('\n'))
        args = filter(len, args)
        process_arguments = process_parser.parse_args(args)
        return process_arguments

    def run_corpus(self, filename=None):
        """ Run the process all over the corpus also evaluate and report if
        are selected.
        :param filename: The name of the config file

        """
        parser = self.parse_cmd_arguments()
        if filename:
            arguments = parser.parse_args(
                open(filename, "r").read().split("\n"))
        else:
            arguments = parser.parse_args()
        self.arguments = arguments
        process_parser = self.parser_generator()
        if arguments.thread:
            process_arguments = None
            if arguments.thread_config:
                process_arguments = self.rebuild_tread_parameter(
                    arguments.thread_config, arguments.common, process_parser)
            logger.debug("File: %s", arguments.thread_file)
            logger.debug("Arguments: %s", process_arguments)
            self.process_file_function(arguments.thread_file, process_arguments)
        else:
            logger.info("Process")
            files = self._create_file_list(options=arguments)
            logger.info("Files: %s", len(files))

            for config in arguments.config:
                self.process_files(
                    file_list=files, config=config, common=arguments.common,
                    jobs=arguments.jobs)
                if arguments.evaluate:
                    logger.info("Evaluation")
                    process_arguments = self.rebuild_tread_parameter(
                        config, arguments.common, process_parser)
                    self.evaluate(arguments, process_arguments)
            if arguments.report:
                logger.info("Report generation")
                self.report(arguments)

    def evaluate(self, experiment_pack, experiment):
        """ Call the user defined evaluation function
        :param experiment_pack: The
        :param experiment:
        """
        self.evaluation_script(experiment_pack, experiment)

    def report(self, experiment_pack):
        """ Call the user defined report function

        :param experiment_pack:
        """
        self.report_script(experiment_pack)

    @staticmethod
    def send_mail(mail_server, from_email, to_emails, body, subject):
        """ Send a mail using SMTP mail server.

        :param mail_server: The server that delivers the mail
        :param subject: A subject added to the email
        :param from_email: A email direction
        :param to_emails: A LIST of email directions
        :param body: The text of the mail.
        """
        subject = 'Subject: {0}\n'.format(subject)
        server = smtplib.SMTP(mail_server)

        return server.sendmail(from_email, to_emails, subject + body)
