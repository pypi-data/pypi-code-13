import pika;
class Rabbitmq:
    host='localhost';
    port=5672;
    vhost='/';
    username='guest';
    password='guest';
    queue="scheduling";
    exchange="scheduling";
    routing="scheduling";
    credentialObj="";
    parametersObj="";
    connectionObj="";
    channelObj="";
    def __init__(self,RabbitmqSettingsDictionary):
        self.host=RabbitmqSettingsDictionary.host;
        self.port=RabbitmqSettingsDictionary.port;
        self.vhost=RabbitmqSettingsDictionary.vhost;
        self.username=RabbitmqSettingsDictionary.username;
        self.password=RabbitmqSettingsDictionary.password;
        self.queue=RabbitmqSettingsDictionary.queue;
        self.exchange=RabbitmqSettingsDictionary.exchange;
        
    def initiate(self):
        self.setCredentials();
        self.setParameters();
        self.setConnection();
        
    def setCredentials(self):
        self.credentialObj=pika.PlainCredentials(self.username,self.password);
        
    def setParameters(self):
        self.parametersObj=pika.ConnectionParameters(self.host,self.port,self.vhost,self.credentialObj);
    
    def setConnection(self):
        self.connectionObj=pika.BlockingConnection(self.parametersObj);
    
    def setChannel(self):
        self.channelObj = self.connectionObj.channel()
        
    def setQueue(self):
        self.channelObj.queue_declare(self.queue,False,True)
    
    def setExchange(self):
        self.channelObj.exchange_declare(self.exchange,"direct",False,True);
        
    def publish(self,body='Hello World! testing'):
        self.initiate();
        self.setChannel();
        self.setQueue();
        self.setExchange();
        self.routing=self.queue+"_routing";
        self.channelObj.queue_bind(self.queue,self.exchange,self.routing);
        self.channelObj.basic_publish(self.exchange,self.routing,body)

