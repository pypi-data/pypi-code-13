

import os
from filebridge import FileBridge
from themeparser import ThemeParser


class Main:
    
    
    __BUILDINTHEMEPATH__=os.path.join(os.path.dirname(os.path.realpath(__file__)),'../themes')
    
    def __init__(self, argParser):
        args=argParser.parse_args()
        if args.clean:
            self.cleanConfigFile(os.path.join(os.environ["HOME"],".i3/config"))
        elif args.list:
            for theme in self.getBuildInTheme():
                print theme
        elif args.file != None:
            self.initParserAndBridge(args.file)
            self.applyTheme()
        elif args.theme != None:
            themesFilePath=os.path.join(self.__BUILDINTHEMEPATH__,args.theme)
            self.initParserAndBridge(themesFilePath)
            self.applyTheme()
        else:
            argParser.print_help()
            exit(0)
            
            
    def initParserAndBridge(self, themeFilePath):
        """
            Init theme parser and file bridge with error handling.
        """
        try:
            self.themeParser=ThemeParser(themeFilePath)
            try:
                self.fileBridge=FileBridge(self.themeParser)
            except Exception as exception:
                print exception.__str__()
                exit(1)
        except Exception as exception:
            print "Failed to load theme:"
            print exception.__str__()
            exit(1)


    def getBuildInTheme(self):
        themes=[]
        for root, dirs, files in os.walk(self.__BUILDINTHEMEPATH__):
                for file in files:
                    themes.append(file)
        return themes
   
    def cleanConfigFile(self,configFilePath):
        try:
            print "Cleaning configuration file..."
            FileBridge.cleanConfigFile(configFilePath)
            print "Done !"
        except Exception as exception:
            print exception.__str__()
            exit(1)
   
    
    def applyTheme(self):
        """
            Apply a theme
        """
        try:
            print "Apply theme"
            self.fileBridge.apply()
            print "Done !"
        except Exception as exception:
            print "Error during theme apply :"
            print exception.__str__()
            exit(1)