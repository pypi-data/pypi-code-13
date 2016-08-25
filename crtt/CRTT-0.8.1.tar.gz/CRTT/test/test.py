#!/usr/bin/python3
import sys,os
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'CRTT_lib'))
#sys.path.append('/root/redfish/CRTT_WS')

from CRTT.config import CONF
from datetime import datetime
from CRTT.loglib import logger
from CRTT.get_nodes import GET_NODE
import multiprocessing
import sys
VERSION = '1.0.0'


def GET_NODE_wraper(cycle,node_path=None):
	msg="SCAN ALL THE NODES IN CYCLE: {0:d}".format(cycle)
	logger.info(msg)
	get_node=GET_NODE(CONF.REST.host,CONF.REST.client_app_ver,CONF.REST.bind_port)
	return get_node.scan_node(node_path)

def compare_url(last_url=None,new_url=None):
	diff_url_str=""

	if len(last_url)<len(new_url):
		for url in list(set(new_url)-set(last_url)):
			diff_url_str+="\n\t"+url
		msg="New node has been found:<hl>{0:s}</hl>".format(diff_url_str)
	else:
		for url in list(set(last_url)-set(new_url)):
			diff_url_str+="\n\t"+url
		msg="Missed node:<hl>{0:s}</hl>".format(diff_url_str)

	logger.warning(msg)

FIRST_CALLED=True
last_url=[]
def GET_NODE_callback(new_url):
	global FIRST_CALLED
	global last_url

	if not FIRST_CALLED:
		if last_url!=new_url:
			compare_url(last_url,new_url)
	last_url=new_url

	FIRST_CALLED=False
	
	
def main():

	if CONF.MAIN.processes:
		try:
			processes=int(CONF.MAIN.processes)
		except ValueError:
			print('Wrong defined processes in conf file')
			sys.exit()
	else:
		processes=multiprocessing.cpu_count()

	cycle=CONF.MAIN.cycle
	use_processes=lambda t: cycle if t+processes>=cycle else t+processes

	if CONF.REST.root_node:
		node_path=CONF.REST.root_node
	else: node_path=None

	for i in range(0,cycle,processes):
		pool = multiprocessing.Pool(processes)
		for t in range(i,use_processes(i),1):
			pool.apply_async(GET_NODE_wraper,(t,node_path), callback=GET_NODE_callback)
		pool.close()
		pool.join()
		if CONF.CLI.time_to_stop:
			if datetime.now()>datetime.strptime(CONF.CLI.time_to_stop,\
				'%Y-%m-%d %H:%M:%S'):
				break

if __name__=="__main__":
	main()
