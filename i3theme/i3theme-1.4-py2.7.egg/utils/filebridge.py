

import os, subprocess,re



class FileBridge:
    """
        Class to convert a theme to an understandable configuration for i3.
        This class can also apply a theme (act on a configuration file).
    """
    
    
    def __init__(self, themeParser, configFilePath=None):
        self.theme=themeParser.getTheme()
        if configFilePath == None:
            self.configFilePath=os.path.join(os.environ["HOME"],".i3/config")



    def getBarConfig(self):
        """
            Build the color block configuration (in the block bar)
        """
        configFormat="colors {\n"
        configFormat+="\tbackground %s\n" % (self.theme["bar_colors"]["background"])
        configFormat+="\tseparator %s\n" % (self.theme["bar_colors"]["separator"])
        configFormat+="\tstatusline %s\n\n" % (self.theme["bar_colors"]["statusline"])


        for barType, barValues in self.theme["bar_colors"].iteritems():
            if(type(barValues) is dict):
                    configFormat+="\t%s"%(barType)
                    for key in ["border", "background", "text"]:
                        color=self.theme["bar_colors"][barType][key]
                        if color[0] != '#':
                            configFormat+=" $%s" % (color)
                        else:
                            configFormat+=" %s" % (color)
                    configFormat+="\n"
            else:
                configFormat+="\t%s"%(barType)
                color=self.theme["bar_colors"][barType]
                if color[0] != '#':
                    configFormat+=" $%s" % (color)
                else:
                    configFormat+=" %s" % (color)
                configFormat+="\n"
        configFormat+="}"
        return configFormat
    
    
      
    def getWindowConfig(self):
        configFormat=""
        for windowType, windowValues in self.theme["window_colors"].iteritems():
            configFormat+="client.%s"%(windowType)
            
            
            for key in ["border","background","text","indicator"]:
                if self.theme["window_colors"][windowType][key][0] != "#":
                    configFormat+=" $%s"%(self.theme["window_colors"][windowType][key])
                else:
                        configFormat+=" %s"%(self.theme["window_colors"][windowType][key])

            configFormat+="\n"
        return configFormat
    
    
    def apply(self):
        """
            Apply theme to config file
        """
        if(os.path.isfile(self.configFilePath)):
            # Remove all previous theme from config file
            FileBridge.cleanConfigFile(self.configFilePath)
            # Open config file
            configFile=open(self.configFilePath, "r+")
            # Apply color config at the begining of the file and the window color config
            configFileContent=self.getColorConfig()+configFile.read()+self.getWindowConfig()
            # Apply bar color config
            s = re.compile('\n(\s)*bar.*{', re.DOTALL)
            configFileContent=re.sub(s,"\nbar { \n"+self.getBarConfig(),configFileContent)   
            # Erase file content and apply change and close file
            configFile.seek(0)
            configFile.truncate()         
            configFile.write(configFileContent)
            configFile.close()
            # Reload configuration
            FileBridge.reloadConfig()
 
    @staticmethod
    def reloadConfig():
        try:
            subprocess.Popen(["i3-msg", "reload"], stdout=subprocess.PIPE)
        except:
            print "i3-msg not found. Please install it to be able to reload the configuration."

 
 
    @staticmethod
    def cleanConfigFile(configFilePath):
        """
            Clear all theme informations from a configuration file
        """
        if(os.path.isfile(configFilePath)):
            # Open file and get content
            configFile=open(configFilePath, "r+")
            # Remove all client config line
            configFileContent=re.sub(r'client\..*\n', "",configFile.read())
            # Remove all variables containing color assignment
            configFileContent=re.sub(r'set.*\#.*\n', "",configFileContent)
            # Remove the color block
            expr = re.compile('(colors[^}]*\}[^\n]*\n)?',re.DOTALL)
            configFileContent=re.sub(expr, "",configFileContent)
            # Erase file content and apply change and close file
            configFile.seek(0)
            configFile.truncate() 
            configFile.write(configFileContent)
            configFile.close()
                 

    def getColorConfig(self):
        """
            Build color variable assignment
        """
        configFormat=""

        if "colors" in self.theme:
            for varName, varValue in self.theme["colors"].iteritems():
                configFormat+="set $%s %s\n" % (varName, varValue)
        return configFormat