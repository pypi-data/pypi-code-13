

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
            Apply configuration to config file
        """
        if(os.path.isfile(self.configFilePath)):
            configFile=open(self.configFilePath, "r+")
            configFileContent=FileBridge.clearColorsEntry(configFile.read())
            configFileContent+=self.getWindowConfig()
            configFile.close()
            configFile=open(self.configFilePath, "w")
            configFileContent=self.getColorConfig()+configFileContent
            s = re.compile('\n(\s)*bar.*{', re.DOTALL)

            configFileContent=re.sub(s,"\nbar { \n"+self.getBarConfig(),configFileContent)  
            configFile.write(configFileContent)
            configFile.close()
            subprocess.Popen(["i3-msg", "reload"], stdout=subprocess.PIPE)
        
    
    @staticmethod
    def cleanConfigFile():
        configFilePath=os.path.join(os.environ["HOME"],".i3/config")
        if(os.path.isfile(configFilePath)):
            configFile=open(configFilePath, "r")
            configFileContent=FileBridge.clearColorsEntry(configFile.read())
            configFile.close()
            configFile=open(configFilePath, "w")
            configFile.write(configFileContent)       
            configFile.close()

    
    @staticmethod
    def clearColorsEntry(conf):
        conf=re.sub(r'client\..*\n', "",conf)
        conf=re.sub(r'set.*\#.*\n', "",conf)
        s = re.compile('(colors[^}]*\}[^\n]*\n)?',re.DOTALL)
        conf=re.sub(s, "",conf)
        return conf

    def getColorConfig(self):
        configFormat=""

        if "colors" in self.theme:
            for varName, varValue in self.theme["colors"].iteritems():
                configFormat+="set $%s %s\n" % (varName, varValue)
        return configFormat