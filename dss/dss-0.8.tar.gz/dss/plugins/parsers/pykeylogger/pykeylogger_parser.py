from core.parsers.parser import Parser
import os, subprocess

class PyKeyloggerParser(Parser):

    def __init__(self, plugin):
        super(PyKeyloggerParser, self).__init__(plugin)
        self.parsed_folder = self.parsed_folder.replace("output.txt", "")
        self.click_dir = os.path.join(self.file_or_dir, "click_images")
        self.file_or_dir = os.path.join(self.file_or_dir, "detailed_log", "logfile.txt")
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keylogger_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keylogger_parser.sh")

    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder, self.click_dir], cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.call([self.script_file, self.file_or_dir, self.parsed_folder, self.click_dir])
