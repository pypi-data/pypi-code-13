from core.parsers.parser import Parser
import os
import subprocess


class ManualScreenShotParser(Parser):
    type = "parsers.ManualScreenShot"

    def __init__(self, plugin):
        super(ManualScreenShotParser, self).__init__(plugin)
        if os.name == 'nt':
            self.script_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "manualscreen_parser.bat")
        else:
            self.script_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "manualscreen_parser.sh")
        self.click_dir = os.path.join(self.file_or_dir, "")
        self.path = self.parsed_folder.replace("output.txt", "")

    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.click_dir, self.path], cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            subprocess.call([self.script_file, self.click_dir, self.path])
