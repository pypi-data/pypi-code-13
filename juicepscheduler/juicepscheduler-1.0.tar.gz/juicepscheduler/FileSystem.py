import os;

class Files:

    directory="/";
    
    def __init__(self,FileSystemSettingsObj):
        self.directory=FileSystemSettingsObj.directory;

    def getFiles(self):
        name=[];
        for filename in os.listdir(self.directory):
            name.append(filename);
        return name;

    def getNumericNamedFiles(self):
        numericFiles=[];
        for filename in self.getFiles():
            filename=u""+filename;
            if(filename.isnumeric()):
                numericFiles.append(filename);
        return numericFiles;
    def getFileContent(self,filepath):
        if(filepath!=""):
            file=open(filepath,"r");
            return file.read();
        
    def remove(self,filepath=""):
        if(filepath!=""):
            os.remove(filepath);
        
