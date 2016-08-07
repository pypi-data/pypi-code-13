#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
#sys.path.append("..")
from net_evi_agent.model import classes
from net_evi_agent.utils.strfunc import strPartition,strSplitToDict

def getV2Config(component):
	model=""
        extra_info_key_list=[""]
        extra_info_dict={}
	neutron_conf=open("/etc/neutron/neutron.conf","r")
	for line in neutron_conf:
		if not line.startswith("#"):
			if "core_plugin" in line:
				strSplitToDict(extra_info_dict,line,"=")
#				print extra_info_dict
		else:
			continue
	#check neutron core plugin if core plugin is ml2,then read info from the file
#	return
	if extra_info_dict['core_plugin'] == "ml2":
		extra_dict={}
        	ml2_conf=open("/etc/neutron/plugins/ml2/ml2_conf.ini","r")
		for line in ml2_conf:
			if not line.startswith("#"):
				tup=strPartition(line,"=")
				#print tup
				if tup[0].strip() == "tenant_network_type":
					model = tup[2].strip()
#					print model
				elif tup[0].strip() == "tunnel_type":
					model = tup[2].strip()
#					print model
				elif tup[0].strip() == "bridge_mappings":
					extra_dict["bridge_mappings"]=tup[2].strip()
				elif tup[0].strip() == "network_vlan_ranges":
					extra_dict["network_vlan_ranges"]=tup[2].strip()
				elif tup[0].strip() == "tunnel_id_ranges":
					extra_dict["tunnel_id_ranges"]=tup[2].strip()
				elif tup[0].strip() == "flat_networks":
					extra_dict["flat_networks"]=tup[2].strip()
				elif tup[0].strip() == "vni_ranges":
					extra_dict["vni_ranges"]=tup[2].strip()
				elif tup[0].strip() == "local_ip":
					extra_dict["local_ip"]=tup[2].strip()
				elif tup[0].strip() == "enable_tunneling":
					extra_dict["enable_tunneling"]=tup[2].strip()
				elif tup[0].strip() == "mechanism_drivers":
					extra_dict["mechanism_drivers"]=tup[2].strip()
				else:
					continue
#		print extra_dict
		extra_info_dict["mechanism_drivers"]=extra_dict["mechanism_drivers"]
		if model == "vlan":
			extra_info_dict["bridge_mappings"]=extra_dict["bridge_mappings"]
			extra_info_dict["network_vlan_ranges"]=extra_dict["network_vlan_ranges"]
		elif model == "gre":
			extra_info_dict["tunnel_id_ranges"]=extra_dict["tunnel_id_ranges"]
			extra_info_dict["local_ip"]=extra_dict["local_ip"]
			extra_info_dict["enable_tunneling"]= extra_dict["enable_tunneling"]
		elif model == "vxlan":
			extra_info_dict["vni_ranges"]=extra_dict["vni_ranges"]
		elif model == "flat":
			extra_info_dict["flat_networks"]=extra_dict["flat_networks"]
		else:
			print "model error"

#		print extra_info_dict
		
		configObj=classes.ConfigNetworkV2(component,model,extra_info_dict)
		return configObj
#def getV3Config():

if __name__=="__main__":
	getV2Config("Neutron")	
