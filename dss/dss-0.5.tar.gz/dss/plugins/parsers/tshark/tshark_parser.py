from core.parsers.parser import Parser
import os, subprocess

class TSharkParser(Parser):
    type = "parsers.TShark"

    def __init__(self, plugin):
        super(TSharkParser, self).__init__(plugin)
        self.parsed_folder = self.parsed_folder.replace("output.txt", "")
        self.batch_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tshark_parser.bat")

    def do_file(self, file_path):
        popen = subprocess.Popen(
            [self.batch_file, file_path, self.parsed_folder], cwd=os.path.dirname(os.path.realpath(__file__)),
            stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
