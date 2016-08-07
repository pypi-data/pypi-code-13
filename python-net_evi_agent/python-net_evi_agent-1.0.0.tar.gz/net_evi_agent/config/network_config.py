#!/usr/bin/python
# -*- coding: UTF-8 -*-
import nova_network
import neutron_network
import sys
#sys.path.append("..")
from net_evi_agent.model.classes import ConfigNetworkV2
#from classes import ConfigNetworkV2 
def getConfigInfo():
	config_file=open("/etc/nova/nova.conf","r")
	global network_component
	for line in config_file:
	#	print line
		if "network_api_class" in line:
        		str_frag=line.partition("=")
	#		print line
			if "neutron" in str_frag[2]:
				network_component="Neutron"
			elif "quantum" in str_frag[2]:
				network_component="Quantum"
			else:
				network_component="NovaNetwork"
	if network_component=="NovaNetwork":
		config2Obj=nova_network.getV2Config(network_component)
#		config2Obj.displayConfigNetworkV2Info()
		#return config2Obj
	elif network_component=="Neutron":
		#print "***"
		config2Obj=neutron_network.getV2Config(network_component)
#		config2Obj.displayConfigNetworkV2Info()	
	else:
		print "network component error"
	return config2Obj
getConfigInfo()
