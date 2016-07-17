#!/usr/bin/python

import yaml,os,re,subprocess
from voluptuous import Schema, Required

class ThemeParser:
    """
        Theme parser used to check and read a theme file.
    """
    
    def __init__(self, themeFilePath):
        """
            Initialise a ThemeParser
        """
        try:
            # Open theme file
            themeFile=open(themeFilePath, "r")
            themeFileContent=themeFile.read()
            themeFile.close()
            
            # Load yaml theme as array
            self.theme=yaml.load(themeFileContent)
                
            # Build theme schema
            self.buildThemeSchema()
            # Try to validating theme
            self.schema(self.theme)

            
        except Exception as exception:
            print "Error during the loading of \"" + os.path.basename(themeFilePath) + "\" :"
            print exception.__str__()
            exit(1)
    
    
    def buildThemeSchema(self):
        """
            Build the validating schema
        """
        window_colors_leaf={
                           Required("border"):str,
                           Required("background"):str,
                           Required("text"):str,
                           Required("indicator"):str
                           }
        bar_colors_leaf={
                           Required("border"):str,
                           Required("background"):str,
                           Required("text"):str
                           }
        
        self.schema=Schema({
                        "meta":{
                                    "author":str,
                                    "version":int,
                                    "description":str
                                },    
                        Required("window_colors"): {
                                                    Required("focused"):window_colors_leaf,
                                                    Required("focused_inactive"):window_colors_leaf,
                                                    Required("unfocused"):window_colors_leaf,
                                                    Required("urgent"):window_colors_leaf
                                                   },
                        Required("bar_colors"): {
                                                    Required("focused_workspace"):bar_colors_leaf,
                                                    Required("active_workspace"):bar_colors_leaf,
                                                    Required("inactive_workspace"):bar_colors_leaf,
                                                    Required("urgent_workspace"):bar_colors_leaf
                                                   }
                       
                       
                       },extra=True)
    
    
    def getTheme(self):
        """
            Get the loaded theme
        """
        return self.theme
    
   
        
  