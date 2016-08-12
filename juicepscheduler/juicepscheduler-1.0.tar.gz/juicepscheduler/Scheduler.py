import time;
from FileSystem import Files;
from Distributor import Distribute;
from Distributor import Destination;
from Settings import FilesSettings;
from Settings import DistributorSettings;
from Settings import RabbitmqSettings;

class Scheduler(Files):

    now=0;
    allFiles=[];
    allThreads=[];
    
    numericFiles=[];
    
    readyToSendFiles=[];
    readyToSendThreads=[];
    
    readyToScheduleFiles=[];
    readyToScheduleThreads=[];
    
    fileSettingsObj="";
    destinationSettingsObj="";
    destinationInnerSettingsObj="";
    
    def __init__(self,FileSystemSettingsObj):
        Files.__init__(self,FileSystemSettingsObj);
        self.now = int(time.time());
        self.fileSettingsObj=FileSystemSettingsObj;
        print("Current time: "+str(self.now));
        
    def setNumericNamedFiles(self):
        self.numericFiles=self.getNumericNamedFiles()
        for filename in self.numericFiles:
            if(int(self.now) < int(filename)):
                self.readyToSendFiles.append(filename);
            else:
                self.readyToScheduleFiles.append(filename);

    def distributeThreads(self):
        for filename in self.numericFiles:
            if(filename.isnumeric()):
                if(self.now>=int(filename)):
                    distributorObj=Distribute(filename+"",filename+"",0);
                    self.allThreads.append(distributorObj.makeThread(
                        self.destinationSettingsObj,
                        self.destinationInnerSettingsObj,
                        self.fileSettingsObj));
                    self.readyToSendThreads.append(distributorObj.makeThread(
                        self.destinationSettingsObj,
                        self.destinationInnerSettingsObj,
                        self.fileSettingsObj));
                else:
                    distributorObj=Distribute(filename+"",filename+"",(int(filename)-self.now));
                    self.allThreads.append(distributorObj.makeThread(
                        self.destinationSettingsObj,
                        self.destinationInnerSettingsObj,
                        self.fileSettingsObj));
                    self.readyToScheduleThreads.append(distributorObj.makeThread(
                        self.destinationSettingsObj,
                        self.destinationInnerSettingsObj,
                        self.fileSettingsObj));

    def schedule(self):
        self.setNumericNamedFiles();
        self.distributeThreads();
    
    def registerDestination(self,destinationSettingsObj):
        self.destinationSettingsObj=destinationSettingsObj;
        
    def registerDestinationSettings(self,destinationInnerSettingsObj):
        self.destinationInnerSettingsObj=destinationInnerSettingsObj;
        
    def start(self):
        for distributorObj in self.allThreads:
            print("Scheduling: "+str(distributorObj.name)+" in "+str(distributorObj.counter)+" seconds!");
            distributorObj.start();
                    
    def startScheduled(self):
        for distributorObj in self.readyToScheduleThreads:
            print("Scheduling: "+str(distributorObj.name)+" in "+str(distributorObj.counter)+" seconds!");
            distributorObj.start();
                    
    def startAwaiting(self):
        for distributorObj in self.readyToSendThreads:
            print("Scheduling: "+str(distributorObj.name)+" in "+str(distributorObj.counter)+" seconds!");
            distributorObj.start();
