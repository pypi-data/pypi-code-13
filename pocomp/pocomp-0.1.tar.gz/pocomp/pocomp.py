import os
import sys

import polib

root_dir = sys.argv[1]

for file in os.listdir(root_dir):
    if file.split(".")[-1] == "po":
        file_name = file.split(".")[0]
        po = polib.pofile("{}{}".format(root_dir, file))
        po.save_as_mofile("{}{}.{}".format(root_dir, file_name, "mo"))
        sys.stdout.write("UPDATED {}{}.mo\n".format(root_dir, file_name))