from core.parsers.parser import Parser
import os
import subprocess


class TSharkParser(Parser):
    type = "parsers.TShark"

    def __init__(self, plugin):
        super(TSharkParser, self).__init__(plugin)
        self.parsed_folder = self.parsed_folder.replace("output.txt", "")
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.sh")

    def do_file(self, file_path):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, file_path, self.parsed_folder], cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.call([self.script_file, file_path, self.parsed_folder])
