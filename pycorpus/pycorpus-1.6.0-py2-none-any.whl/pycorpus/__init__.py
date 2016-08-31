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
  don't use the sys.out. Logging using a Filehandler may do the trick.

"""

import os
import configargparse
import subprocess
import smtplib
from multiprocessing import Process
from logging import getLogger

__author__ = 'Josu Bermúdez <josu.bermudez@deusto.es>'
__created__ = '06/2013'

logger = getLogger("pycorpus")


class CorpusProcessor:
    """ The class that manages the parallel process of all files of the corpus.
    Also have useful functions like send_mail and launch.
    """
    separator = ":"

    def __init__(self, generate_parser_function, process_file_function,
                 evaluation_script=None, report_script=None):
        self.parser_generator = generate_parser_function
        self.process_file_function = process_file_function
        self.evaluation_script = evaluation_script
        self.report_script = report_script
        self.arguments = None

    @staticmethod
    def parse_cmd_arguments():
        """ Parse command line arguments and put options into a object.
        """
        parser = configargparse.ArgumentParser(description="Process a text file or a \
            directory tree of files using multriprocess")
        parser.add_argument(
            '-p', '--parameters', is_config_file=True,
            help='Config file path ')
        parser.add_argument(
            '--jobs', dest='jobs', action='store', default=8,
            help="Set the max number of parallel process.")
        parser.add_argument(
            '--file', dest="files", action='append', default=[],
            help="File to processed. May be used multiple times and"
                 "with directory parameter. ")
        parser.add_argument(
            '--directory', dest='directories', action="append",
            default=[],
            help="All the files contained by the directory(recursively) "
                 "are processed. May be used multiple times and with"
                 "the file parameter.")
        parser.add_argument(
            '--extension', dest='extensions', action='append',
            default=[],
            help="The extensions of the files(without dot) that must "
                 "be processed form directories. The '*' is used as accept "
                 "all. May be used multiple times ."
                 "WARNING doesn't filter files from --files.")
        parser.add_argument(
            '--config', dest='config', action='append', default=[],
            help="The config files that contains the parameter each experiment."
                 "Use '{0}' to use multiple files in one experiment. Repeat "
                 "the parameter for multiple experiments."
            .format(CorpusProcessor.separator))
        parser.add_argument(
            '--common', dest='common', action='store', default="",
            help="A common config for all experiments."
                 "May be multiple files separated by '{0}'"
            .format(CorpusProcessor.separator))
        parser.add_argument(
            '--evaluate', dest='evaluate', action='store_true',
            help="Activates the evaluation.")
        parser.add_argument(
            '--report', dest='report', action='store_true',
            help="Activates report system.")
        return parser

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

    def rebuild_tread_parameter(self, thread_config, common, process_parser):
        config_files = [arg_file for arg_file in common.split(self.separator) + thread_config.split(self.separator)]
        wrapper_parser = configargparse.ArgumentParser(parents=[process_parser],
                                                       default_config_files=config_files, add_help=False)
        # Only process the config files
        process_arguments = wrapper_parser.parse_args(args="")
        return process_arguments

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

    def process_files(self, file_list, process_arguments, jobs=8):
        """Call a process that executes process function over selected files
        with the config argument

        :param jobs: The maximun number of concurrent jobs
        :param file_list: The list of files to process.
        :param process_arguments: The arguments to process the files
        """

        running = []
        logger.info("loading workers")
        while file_list or running:
                while len(running) < jobs and file_list:
                    filename = file_list.pop()
                    p = Process(target=self.process_file_function, name=filename, args=(filename, process_arguments))
                    p.start()
                    running.append(p)
                for p in running:
                    if not p.is_alive():
                        running.remove(p)
                        if p.exitcode != 0:
                            logger.info("Process %s finished with errors", p.name)
                        else:
                            logger.info("Process %s finished", p.name)
        logger.info("Corpus Processed")

    def run_corpus(self, filename=None):
        """ Run the process all over the corpus also evaluate and report if
        are selected.
        :param filename: The name of the config file

        """
        parser = self.parse_cmd_arguments()
        if filename:
            arguments = parser.parse_args(
                config_file_contents=open(filename, "r").read().split("\n"))
        else:
            arguments = parser.parse_args()
        self.arguments = arguments
        process_parser = self.parser_generator()
        logger.info("Process")
        files = self._create_file_list(options=arguments)
        logger.info("Files: %s", len(files))
        for config in arguments.config:
            process_arguments = self.rebuild_tread_parameter(
                config, arguments.common, process_parser)
            self.process_files(
                file_list=files, process_arguments=process_arguments, jobs=arguments.jobs)
            if arguments.evaluate:
                logger.info("Evaluation")
                process_arguments = self.rebuild_tread_parameter(
                    config, arguments.common, process_parser)
                self.evaluate(arguments, process_arguments)
        if arguments.report:
            logger.info("Report generation")
            self.report(arguments)
