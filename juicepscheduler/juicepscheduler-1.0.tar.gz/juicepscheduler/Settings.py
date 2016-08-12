class FilesSettings:
    directory="";
    def __init__(self,settingsDictionary):
        self.directory=settingsDictionary["directory"];

class DistributorSettings:
    destination="";
    def __init__(self,destinationDictionary):
        self.destination=destinationDictionary["destination"]
        
class RabbitmqSettings:
    host="";
    port="";
    vhost="";
    username="";
    password="";
    queue="";
    exchange="";
    def  __init__(self,settingsDictionary):
        self.host=settingsDictionary["host"];
        self.port=settingsDictionary["port"];
        self.vhost=settingsDictionary["vhost"];
        self.username=settingsDictionary["username"];
        self.password=settingsDictionary["password"];
        self.queue=settingsDictionary["queue"];
        self.exchange=settingsDictionary["exchange"];