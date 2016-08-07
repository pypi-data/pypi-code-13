#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
#sys.path.append("..")
from net_evi_agent.model.classes import ConfigNetworkV2
from net_evi_agent.utils.strfunc import strPartition,strSplitToDict

def getV2Config(component):
	model=""
	extra_info_key_list=["network_manager","vlan_interface","vlan_start","routing_source_ip","allow_same_net_traffic","flat_interface","flat_network_bridge","fixed_range","my_ip","floating_range","multi_host"]
	extra_info_dict={}
	nova_conf=open("/etc/nova/nova.conf","r")
	for line in nova_conf:
		for item in extra_info_key_list:
			if item in line:
				if item == "network_manager":
					network_manager=strPartition(line,"=")
		                        print network_manager
                		        if "Vlan" in network_manager[2]:
                               	 		model="VLAN"                            
                        		elif "flatDHCP" in network_manager[2]:
                                		model="FLATDHCP"
                        		else:
                                		model="FLAT"
					print model
				elif (item == "vlan_interface" or item == "vlan_start" or item == "routing_source_ip" or item =="allow_same_net_traffic"):
					if model == "VLAN":
						strSplitToDict(extra_info_dict,line,"=")
				elif (item == "flat_interface" or item == "flat_network_bridge"):
					if model == "FLATDHCP" or model == "FLAT":
						strSplitToDict(extra_info_dict,line,"=")
				else:
					 strSplitToDict(extra_info_dict,line,"=")
	print extra_info_dict
	configObj=ConfigNetworkV2(component,model,extra_info_dict)
	return configObj

if __name__=="__main__":
	configNetV2=getV2Config("NovaNetwork")
	configNetV2.displayConfigNetworkV2Info()
