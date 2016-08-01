from core.parsers.parser import Parser

import os, subprocess

class ManualScreenShotParser(Parser):
    type = "parsers.ManualScreenShot"

    def __init__(self, plugin):
        super(ManualScreenShotParser, self).__init__(plugin)
        self.batch_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "manualscreen_parser.bat")
        self.click_dir = os.path.join(self.file_or_dir, "")
        self.path = self.parsed_folder.replace("output.txt", "")

    def parse(self):
        popen = subprocess.Popen(
            [self.batch_file, self.click_dir, self.path], cwd=os.path.dirname(os.path.realpath(__file__)),
            stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)

