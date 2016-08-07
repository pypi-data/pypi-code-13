#!/usr/bin/python
# -*- coding:UTF-8 -*-
import sys
import commands
import os
import types
import xml.dom.minidom
from xml.dom import minidom
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import re
#sys.path.append("..")
from net_evi_agent.config import network_config
from net_evi_agent.config import common_config_func
#sys.path.append("/usr/local/multi_tenant/")
#import network_config
#import common_config_func 
from net_evi_agent.model import classes
import traceback
def getTopologyInfo():
	###
	##get network config info
	###
	configObj=network_config.getConfigInfo()
	#configObj.displayConfigNetworkV2Info()
	component=configObj.component
	model=configObj.model
	extra_info=configObj.extra_info	

	###
	##neutron vlan topology
	###
	if component=="Neutron" and model == "vlan":
		print "neutron vlan"
		print extra_info
		if(extra_info["mechanism_drivers"]=="openvswitch"):
			
			#####################################################################################################
			#Get OVS bridges
			#@autho wesia
			#####################################################################################################
			br_int="br-int"
			tup=common_config_func.strPartition(extra_info["bridge_mappings"],":")
			br_eth=tup[2].strip()
			ovsBridges=[]
			print br_eth	

			"""get the ovs bridges info"""
			try:
				(status,result) = commands.getstatusoutput("ovs-vsctl list-br")
				#print type(result) ---string 
				if(status>0):
					print "error in execute command 'ovs-vsctl list-br'"
					exit(1)
				#list_brs=result.split()
			except:
				print "error in execute command 'ovs-vsctl list-br'"
			else:
				list_brs=result.split()
				
			#print list_brs
			if(br_eth not in list_brs):
				print "there is something wrong with the bridge_mapping configuration in compute node"
				exit(1)
			if(br_int not in list_brs):
				print "there is no br-int bridge in the compute node"
				exit(1)
			br_type="ovs-bridge"
			brInt=classes.OvsBridge(br_int,br_type)	
			brEth=classes.OvsBridge(br_eth,br_type)
		#	print brInt.name
			ovsBridges.append(brInt)
			ovsBridges.append(brEth)
			for ovsbr in ovsBridges:
				ovsbr.getPortsOfBridge()
				ovsbr.displayBridgeInfo()		
			#print brInt.bridges_count,brInt.ovs_bridge_counts	

		        
			########################################################################################################
	                #Get VMS info
			#@author wesia
	                ########################################################################################################
			"""get the vms using 'virsh list'"""
			VMS=[]
			try:
				(status,result) = commands.getstatusoutput("virsh list --all")
				#if(status >0):
			except:
				print "error in execute command 'virsh list'"
			else:
				if(result==""):
					print "there is no running vms on the compute node"
					exit(1)
				else:
					#print result
					"""deal with the 'virsh list result' and get a vms list"""
					list_vms=result.split()
					list_vms=list_vms[4:]
					#print list_vms
					#for item in list_vms:
					#	print item
					#print len(list_vms)
					
					"""get the xml file of each vm"""
			
					for i in range(1,len(list_vms),3):
						#print list_vms[i]
						try:
							dumpxml_command="virsh dumpxml "+list_vms[i]+">>"+list_vms[i]+".xml"
							os.system(dumpxml_command)
							#(status,result)=.getstatusoutput(dumpxml_command)	
							#print result
						except:
							print "error in get the xml file of vm"
						else:
							"""deal with the instance xml"""
							xml_file=list_vms[i]+".xml"
							vm_dict={}
							#parser=xml.sax.make_parser()
							#parser.setFeature(xml.sax.handler.feature_namespaces, 0)
							#Handler=classes.VMXmlHandler()
							#parser.setContentHandler(Handler)
							#parser.parse(xml_file)
							#print Handler.vm_name,Handler.vm_interfaces
							try:
								xml_tree = xml.dom.minidom.parse(xml_file)
								collection=xml_tree.documentElement
								name_node = collection.getElementsByTagName("name")[0]
								name=name_node.childNodes[0].data
								#print name
								interfaces = collection.getElementsByTagName("interface")
								ifs_list=[]
								for interface in interfaces:
									attr_list=[]
									if interface.hasAttribute("type"):
										network_type=interface.getAttribute("type")	
										if network_type=="bridge":
											mac=interface.getElementsByTagName("mac")[0].getAttribute("address")
											attr_list.append(mac)
											bridge=interface.getElementsByTagName("source")[0].getAttribute("bridge")
											attr_list.append(bridge)
											dev=interface.getElementsByTagName("target")[0].getAttribute("dev")
											attr_list.append(dev)
									if attr_list:
										ifs_list.append(attr_list)
								vm_dict[name]=ifs_list
								#print vm_dict
								vmObj=classes.VirtualMachine(name,vm_dict[name],list_vms[i+1])
								VMS.append(vmObj)
							except:
								pass
							finally:
								os.system("rm -rf *.xml")	
			if VMS:
				for vm in VMS:
					vm.displayVMInfo()	

	                ########################################################################################################
	                #Get Linux BRIDGES INFO
	                #@author wesia
	                ########################################################################################################
			linuxBridges=[]
			try:
				(status,result) = commands.getstatusoutput("brctl show")
			except:
				print "error in execute command 'brctl show'"
			else:
				"""result is a string ,get the bridge name from result,can not use split,cause,each bridge has different numbers of interfaces,we cannot make sure which element is name"""
				"""get the first word of each line of the result string"""	
				br_name=re.findall(r'\n(\S+)\t',result,re.I|re.M)
				#print br_name		

				for name in br_name:
					lbObj=classes.LinuxBridge(name,"linux-bridge")
					linuxBridges.append(lbObj)
			#print classes.Bridge.bridges_count
			#print classes.LinuxBridge.__bases__
			for lb in linuxBridges:
				lb.getPortsOfBridge()
				lb.displayBridgeInfo()	
	
	

	                #####################################################################################################
	                #Create Topology Tree
	                #@author wesia
	                #####################################################################################################
			objTopo=classes.Topology(VMS,linuxBridges,ovsBridges)	
			objTopo.createTopology()
			#objTopo.displayTopology()
			objTopo.displayTopology(objTopo.tree_root)	

			"obtain the xml file of the topology tree"
			try:
				f=open("ibm1-00-topo-info.xml","w")
				try:
					xmlstr=""
					doc=minidom.Document()
					rootNode=doc.createElement("compute")
					rootNode.setAttribute("name",objTopo.tree_root.name)
					doc.appendChild(rootNode)
					for child in objTopo.tree_root.childlist:
						objTopo.topologyToXML(child,rootNode,doc)	
					
					xmlstr=doc.toprettyxml(indent="    ", encoding="utf-8")	

					doc.writexml(f,"\t","\t","\n","utf-8")
				except:
					traceback.print_exc() 
			except IOError:
				print "open topo file failed"
			finally:
				f.close()
				return xmlstr

str_xml=getTopologyInfo()
print str_xml
