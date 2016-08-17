import os

class PatchExpander(object):
    """expand a patch (or other file) with a keyword"""
    def __init__(self, pattern="\${database\.name}", names_file="names.txt"):
        """initalize the conversion."""
        self.pattern = pattern
        self.names_file = names_file

    def expand(self):
        command = """for file in $(grep """ + self.pattern + """ -lR *) ; do
          line=$(sed -n "/""" + self.pattern + """/p" $file)
          cat """ + self.names_file + """ | while read line2
          do
            linetmp=$(echo $line | sed "s/""" + self.pattern + """/$line2/g")
            sed -i "/""" + self.pattern + """/a $linetmp" $file
          done
          sed -i '/""" + self.pattern + """/d' $file
        done"""
        os.system(command)

if __name__ == "__main__":
    import sys
    args = ['nothing', "\${database\.name}", "names.txt"]
    for x in range(1, len(sys.argv)):
        args[x] = sys.argv[x]
    searcher = PatchExpander(args[1], args[2])
    searcher.expand()
    print("Completed the expansion; check files for result")
