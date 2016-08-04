import logging
import socket
import logstash

host = "logstash"
if host != "logstash":
  # Configured for use with logstash link in docker
  lager = logging.getLogger("Satellite Driver")
  lager.addHandler(logstash.LogstashHandler(host, 5000, version=1))
  lager.setLevel(logging.WARNING)
else:
  # Configure for testing 
  logging.basicConfig()
  lager = logging.getLogger("Testing") 
  lager.setLevel(logging.WARNING)
