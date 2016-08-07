#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.sax
import commands
from xml.dom import minidom
import traceback
import pika
#import topology.topology
class ConfigNetworkV2:
	component=""
	model=""
	extra_info={}
	def __init__(self,component,model,extra_info):
		self.component=component
		self.model=model
		self.extra_info=extra_info
	def displayConfigNetworkV2Info(self):
		print "component:",self.component,"\n","model:",self.model,"\n","extra_info:",self.extra_info,"\n"
class VirtualMachine:
	"virtual machines on the compute node"
	vms_count=0
	def __init__(self,name,macs,status):
		self.name=name
		self.macs=macs
		self.status=status
		self.vlan=""
		VirtualMachine.vms_count+=1
	def setVlan(self,external_vlan_id):
		self.vlan=external_vlan_id
	def displayVMInfo(self):
		print self.name,"\n","---","interfaces:"
		for interface in self.macs:
			print "------",interface[0],interface[1],interface[2]
		print "---status:",self.status,"\n","\n"
			
			
#class VMXmlHandler(xml.sax.ContentHandler):
#	def __init__(self):
#		self.CurrentData=""
#		self.vm_name=""
#		self.vm_interfaces=[]
#		self.network_typ=""
#	def startElement(self,tag,attribute):
#		self.CurrentData=tag
#		#print self.CurrentData
#		interface_dict={}
#		if tag=="interface":
#			self.network_type=attribute["type"]
#		elif tag=="mac" and attribute.has_key("address") and self.network_type=="bridge":
#			key="mac:"+attribute["address"]
#			#interface_dict["mac"]=attribute["address"]
#		elif tag=="source" and attribute.has_key("bridge") and self.network_type == "bridge":
#			if key:
#				interface_dict[key]=attribute["bridge"]
#		else:
#			pass
#		if interface_dict:
#			self.vm_interfaces.append(interface_dict)
#	def endElement(self,tag):
#		self.CurrentData=""
#	def characters(self,content):
#		if self.CurrentData=="name":
#			self.vm_name=content		

class Bridge:
	bridges_count=0
	def __init__(self,name,bridge_type):
		self.name = name
		self.bridge_type=bridge_type
		self.ports = {} 
		Bridge.bridges_count += 1
	def getName(self):
		return self.name
	def setPorts(self,ports):
		self.ports=ports
	def getPortsOfBridge(self):
		pass
	def displayBridgeInfo(self):
		print self.bridge_type," ",self.name,":",self.ports

class OvsBridge(Bridge):
	'ovs bridge'
	ovs_bridge_counts=0
	def __init__(self,name,bridge_type):
		Bridge.__init__(self,name,bridge_type)
		OvsBridge.ovs_bridge_counts += 1
	def getPortsOfBridge(self):
		#print "this function"
		name=self.getName()
		#print name
		try:
			command="ovs-vsctl list-ifaces "+name
			(status,result)=commands.getstatusoutput(command)
			ports=result.split()
			self.setPorts(ports)
		except:
			print "there is some error with getting the ports of the ovsBridge"
		else:
			pass		
class LinuxBridge(Bridge):
	'linux bridge'
	linux_bridge_counts=0
	def __init__(self,name,bridge_type):
		Bridge.__init__(self,name,bridge_type)
		LinuxBridge.linux_bridge_counts += 1
	def getPortsOfBridge(self):
		name=self.getName()
		try:
			command="brctl show "+name
			(status,result)=commands.getstatusoutput(command)
		#	print result.split()[10:]
		except:
			print "there is some errors getting linuxbridges ports"
		else:
			ports=result.split()[10:]
		#	print ports
			self.setPorts(ports)
class TreeNode:
	def __init__(self,name="",childlist=[]):
		self.name=name
		self.childlist=childlist
	def addChild(self,node):
		self.childlist.append(node)
		
class Topology:
	"multi_tenant network topology in openstack"
	def __init__(self,vms,lbs,obs):
		"initital devices in topology"
		self.vms=vms
		self.lbs=lbs
		self.obs=obs
		self.tree_root=TreeNode("ibm1-00",[])
	def createTopology(self):
		"create topology"
		lbNodes={}
		obNodes={}
		for lb in self.lbs:
			lbNodes[lb.name]=TreeNode(lb.name,[])
		for ob in self.obs:
			obNodes[ob.name]=TreeNode(ob.name,[])

		#for key in lbNodes:
		#	print key,lbNodes[key].childlist
		#for key in obNodes:
		#	print key,obNodes[key].childlist


		"link between vm and bridges"
		for vm in self.vms:
			name=vm.name
			interfaces=vm.macs
			for interface in interfaces:
				mac=interface[0]
				br=interface[1]
				dev=interface[2]
				status=vm.status
				print mac,br,dev,status
				for lb in self.lbs:
					if lb.name==br:
						vm_node=TreeNode(mac,[])	
						lbNodes[lb.name].addChild(vm_node)
						#print len(lbNodes[lb.name].childlist)
			#			for child in lbNodes[lb.name].childlist:
							#print child.name
				for ob in self.obs:
					if ob.name==br:
						vm_node=TreeNode(mac,[])
						obNodes[ob.name].adddChild(vm_node)
		
		
		#for lb_node in lbNodes:
		#	print lb_node
		#	for lb_node_child in lbNodes[lb_node].childlist:
		#		print "-->",lb_node_child.name,lb_node_child.childlist
		#for ob_node in obNodes:
		#	print ob_node
		#	for ob_node_child in obNodes[ob_node].childlist:
		#		print "-->",ob_node_child.name,ob_node_child.childlist
	
		
		"link between obs  and lbs"
		lb_port_list={}
		for lb in self.lbs:
			#print lb.ports
			for port in lb.ports:
				if port.startswith("qvb"):
					lb_port_list[port]=lb.name
		#print "linux bridge ports dict:(key is the qvoXXX port and value is the bridge the port belongs to:)",lb_port_list

		for ob in self.obs:
			for port in ob.ports:
				if port.startswith("qvo"):
					#print "the qvoXXX ports on ovs bridges:",port

					"compare qvoXXX with qvbXXX,if same XXX"
					for key in lb_port_list:
						#print "port",port[3:]
						#print "key:",key[3:]
						if key[3:]==port[3:]:
							lb_node=lbNodes[lb_port_list[key]]
							#print lb_node.name,lb_node.childlist	
							"see the child node is already been added to the ob or not,if it has been added then dont not add it again"
							if obNodes[ob.name].childlist:
								for child in obNodes[ob.name].childlist:
									if child.name != lb_node.name:
										obNodes[ob.name].addChild(lb_node)
							else:
								obNodes[ob.name].addChild(lb_node)	
		#for ob in obNodes:
		#	print obNodes[ob].name
		#	print len(obNodes[ob].childlist)
		#	for ob_node_child in obNodes[ob].childlist:
		#		print "-->",ob_node_child.name
					
		"link between obs"
		parent_if=""
		for ob in self.obs:
			if ob.name == "br-int":
				for port in ob.ports:
					"get the port int-br-ethX,br-ethX is the other bridge"
					index=port.find("int")
					#print "index:",index
					if index==0:
						parent_if=port[4:]
						#print parent_if
						ob_node=obNodes[ob.name]
						obNodes[parent_if].addChild(ob_node)
					elif index>0:		
						parent_if="br-tun"
						ob_node=obNodes[ob.name]
						obNodes[parent_if].addChild(ob_node)
					else:
						#print parent_if
						continue
							
			elif ob.name==parent_if:
				ob_node=obNodes[ob.name]
				self.tree_root.addChild(ob_node)	
			else:
				pass

	def displayTopology(self,root):
		"""
		traverse the topology tree:
		print the each node during traversing
		"""
		print root.name
		if root.childlist:
			for child in root.childlist:
				self.displayTopology(child)
		
		#print root.name
		#print len(root.childlist)
		#if root.childlist:
		#	for child in root.childlist:
		#		print "1 depth parent:",child.name
		#		if child.childlist:
		#			for child_2 in child.childlist:
		#				print "2 depth:",child_2.name
		#				if child_2.childlist:
		#					for child_3 in child_2.childlist:
		#	
		#			print "3 depth:",child_3.name

	def topologyToXML(self,topo_node,xml_node,doc):
		try:
			if topo_node.childlist:
				bridgeNode=doc.createElement("bridge")	
				bridgeNode.setAttribute("name",topo_node.name)
				xml_node.appendChild(bridgeNode)
				for child in topo_node.childlist:
					self.topologyToXML(child,bridgeNode,doc)
			else:
				vmNode=doc.createElement("vm")	
				xml_node.appendChild(vmNode)
				vmTextNode=doc.createElement(topo_node.name)
				vmNode.appendChild(vmTextNode)
		except:
			traceback.print_exc()

class Compute:
	"AMQP agent,receive the gathering request from the contrller node plugin"
	def __init__(self):
		self.connection=pika.BlockingConnection(pika.ConnectionParameters(host="172.21.5.34"))
		self.channel=self.connection.channel()
		
		"define the exchange"
		self.channel.exchange_declare(exchange="network_evidence",type="fanout")
		
		"generate a queue randomly to bind with the exchange"
		result = self.channel.queue_declare(exclusive=True)
		self.queue_name=result.method.queue
		print self.queue_name
		self.channel.queue_bind(exchange="network_evidence",queue=self.queue_name)
	def get_response(request):
		if request=="l2-topology_info":
			"get the topology info on this compute node"
					
		elif request=="l2-openflow_BDD":
			str="there is no evidence of openflow on ibm1-00"
		elif request=="l2-sec_group":
			str="there is no evidence of secgroup on ibm1-00"
		else:
			str="check your request!"
			return str
			
	def get_request(self,ch,method,properties,body):
		print "deal with the request received and make response"
		
		print "getting request:",body
		self.response=body
		print properties
		ch.basic_publish(exchange = "",routing_key=properties.reply_to,body=self.response)
		ch.basic_ack(delivery_tag=method.delivery_tag)
	def receive(self):
		self.channel.basic_qos(prefetch_count=1)
		self.channel.basic_consume(self.get_request,queue=self.queue_name)

		print "[*] waiting for request"
		self.channel.start_consuming()
