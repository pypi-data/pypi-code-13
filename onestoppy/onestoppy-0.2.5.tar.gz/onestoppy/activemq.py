import sqlalchemy, consul, traceback, sys

from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync import Stomp

# Example of how to use this library is here:
# http://nikipore.github.io/stompest/sync.html#module-stompest.sync.examples

class Connection:
    client = None
    env = None
    c = consul.Consul(host='consul.service.onestop')

    def __init__(self, env, username=None, password=None, clientid=None):
        self.env = env

	# First test if there is a stomp host/port configuration
	try:
		index, data = self.c.kv.get('global/config/%s/common/ActiveMQ/stomp/host' % self.env)
		stomp_host = data['Value']

		index, data = self.c.kv.get('global/config/%s/common/ActiveMQ/stomp/port' % self.env)
		stomp_port = int(data['Value'])

		stomp_config = StompConfig('tcp://%s:%d' % (stomp_host, stomp_port))
	except:
		pass

	# Then check if there is a full StompConfig entry, if there is use that instead
	try:
		index, data = self.c.kv.get('global/config/%s/common/ActiveMQ/stomp/StompConfig' % self.env)
		configuration = data['Value']

		stomp_config = StompConfig(configuration)
	except:
		pass

	self.client = Stomp(stomp_config)

