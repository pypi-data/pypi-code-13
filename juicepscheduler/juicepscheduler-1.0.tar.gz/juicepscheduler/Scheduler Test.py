from Scheduler import *;

schedulerObj=Scheduler(FilesSettings({"directory":"/home/sahil/Desktop"}));

schedulerObj.registerDestination(DistributorSettings({"destination":"rabbitmq"}));

schedulerObj.registerDestinationSettings(RabbitmqSettings({"port":5672,"host":"localhost","vhost":"/","username":"guest","password":"guest","queue":"scheduling","exchange":"scheduleEx"}));

schedulerObj.schedule();
schedulerObj.start();
