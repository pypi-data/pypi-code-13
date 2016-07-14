#!/usr/bin/python

from utils.themeparser import ThemeParser
from utils.filebridge import FileBridge
from utils.argparser import argParser

import os
from ecdsa.ecdsa import __main__


def main():
    args=argParser.parse_args()


    if args.clean:
        
        print "Cleaning configuration file..."
        FileBridge.cleanConfigFile()
        print "Done !"
    elif args.list:
        themesFolderPath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"themes")
        for root, dirs, files in os.walk(themesFolderPath):
            for file in files:
                print file

    elif args.file != None:
        print "Apply theme"
        themeParser=ThemeParser(args.file)
        fileBridge=FileBridge(themeParser)
        fileBridge.apply()
        print "Done !"
    elif args.theme != None:
        print "Apply theme"
        themesFilePath=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'themes',args.theme)
        themeParser=ThemeParser(themesFilePath)
        fileBridge=FileBridge(themeParser)
        fileBridge.apply()
        print "Done !"



if __name__ == "__main__":
    main()
