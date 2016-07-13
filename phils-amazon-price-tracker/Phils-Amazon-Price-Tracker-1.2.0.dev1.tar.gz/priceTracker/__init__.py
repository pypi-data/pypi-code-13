#!/usr/bin/env python3
import sys
import getopt
from .priceTrackerClass import priceTracker
pClass = priceTracker()
def main(argv):
    from .save_data import createDir
    from .analyse import analyse,readList
    createDir("")
    try:
        opts, args = getopt.getopt(argv,"hi:o:l:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("amazon-tracker.py -i <inputfile> -l <link> -o <outputfile>")
        print("trying to continue ...")
        #sys.exit(2)
    if len(opts) == 0:
        readList()
    else:
        for opt, arg in opts:
            if opt == "-h":
                print("amazon-tracker.py -i <inputfile> -l <link> -o <outputfile>")
                sys.exit()
            elif opt in ("-i"):
                pClass.inputfile=arg
                readList()
            elif opt in ("-o"):
                pClass.outputfile = arg
            elif opt in ("-l"):
                link = arg
                analyse(arg)
            else:
                readList()
    output()
pass
def output():
    from .outputChange import writeDateFile,lastChange
    writeDateFile()
    if pClass.linkFileEntries >= 5:
        lastChange(5)
    else:
        print(str(pClass.linkFileEntries))
        lastChange(1)
pass
