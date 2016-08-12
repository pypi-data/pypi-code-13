import os;
import time;
import threading;

from Worker import Rabbitmq;
from FileSystem import Files;
from Settings import RabbitmqSettings;

class Distribute(threading.Thread):
    
    threadId="";
    threadname="";
    threadCounter="";
    
    fileSettingsObj="";
    destinationSettingsObj="";
    destinationInnerSettingsObj="";
    
    def __init__(self,threadname,threadId,threadCounter):
        self.threadname=threadname;
        self.threadId=threadId;
        self.threadCounter=threadCounter;
    
    def makeThread(self,destinationSettingsObj,destinationInnerSettingsObj,fileSettingsObj):
        threading.Thread.__init__(self);
        self.name=self.threadname;
        self.ThreadID=self.threadId;
        self.counter=self.threadCounter;
        self.fileSettingsObj=fileSettingsObj;
        self.destinationSettingsObj=destinationSettingsObj;
        self.destinationInnerSettingsObj=destinationInnerSettingsObj;
        return self;

    def run(self):
        while self.counter > 0:
            time.sleep(1);
            self.counter-=1;
        if(self.counter==0):
            filepath=self.getFilepath();
            content=self.getContent(filepath);
            DestinationObj=Destination(self.destinationSettingsObj);
            DestinationObj.register(self.destinationInnerSettingsObj);
            DestinationObj.publish(content);
            self.removeFile(filepath);
            
    def removeFile(self,filepath):
        filesObj=Files(self.fileSettingsObj)
        filesObj.remove(filepath);
    
    def getContent(self,filepath):
        filesObj=Files(self.fileSettingsObj)
        return filesObj.getFileContent(filepath);
    
    def getFilepath(self):
        filepath=self.fileSettingsObj.directory+"/"+self.name
        return filepath;
            

class Destination:
    destination="";
    destinationObj="";
    def __init__(self,destinationSettings):
        self.destination=destinationSettings.destination;
        
    def register(self,RabbitmqSettings):
        if(self.destination=='rabbitmq'):
            self.destinationObj= self.registerRabbitmq(RabbitmqSettings);
        else:
            self.destinationObj= self.registerRabbitmq(RabbitmqSettings);
            
    
    def registerRabbitmq(self,RabbitmqSettings):
        return Rabbitmq(RabbitmqSettings);
    
    def publish(self,content):
        self.destinationObj.publish(content);
