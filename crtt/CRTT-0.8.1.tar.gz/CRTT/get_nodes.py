#!/usr/bin/env python3
import sys,os
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'CRTT_lib'))
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from datetime import datetime
from datetime import timedelta
import socket 
import json
from distutils.version import LooseVersion

from CRTT.loglib import logger
#from CRTT_Error import HttpTimeError
from CRTT.retry import retry
from CRTT.config import CONF
import os.path
import configparser
import re,ast
from CRTT.crtt_json import *

socket.setdefaulttimeout(CONF.REQUEST.timeout)
VERSION = '1.0.0'

class GEN_URL():
	'''
	Build complete URL

	:param host: IP address or domain name of the target 
		Rest Server's resource interface.
	:type host: str
	:param path: the path of the URL to access a specific Redfish Node.
		example:'/redfish/v1'
	:type path: str, optional
	:param url: the url of a specific Redfish Node.
		example:'http://10.204.29.221:8888/redfish/v1/Managers/1'
	:type url: str, optional

	:output get_url: return completed URL to access a specific node.
	:type get_url: str
	:output get_path: return path of an URL.
	:type get_url: str
	'''
	supported_rest_versions = CONF.REST.ver_support

	def __init__(self,host,scheme='http',rest_version=None,port=8888):
		self._empty_com=urlparse('')
		self._scheme=scheme
		port=str(port)
		self._netloc=host+":"+port
		self.cli_name = CONF.REST.client_name
		self._rest_version = rest_version
		self.new_url=''

	def _check_rest_version(self, version):
		"""Validate a REST API version is supported by the library and target array."""
		version = str(version)
		if version not in self.supported_rest_versions:
			msg = "Library is incompatible with REST API version {0}"
			raise ValueError(msg.format(version))
		return version

	def _choose_rest_version(self):
		"""Return the latest REST API version supported by target array."""
		return max(self.supported_rest_versions, key=LooseVersion)

	def _gen_rest_ver(self):
		if self._rest_version:
			# check input version whether is in support list
			self._rest_version = self._check_rest_version(self._rest_version)
		else:
			self._rest_version = self._choose_rest_version()

	def get_url(self, path=None):
		if path == None or  path == 'None' or path == '':
			self._gen_rest_ver()
			path="/{0}/v{1}".format(self.cli_name, self._rest_version)
		else:
			current_url=urlparse(path)
			if self._scheme == current_url.scheme or ":" in current_url.netloc:
				self._netloc=current_url.netloc
				return path

		new_url_obj=self._empty_com._replace(scheme='http', netloc=self._netloc,path=path)
		self.new_url= new_url_obj.geturl()
		return self.new_url

	def get_path(self,url=None):
		if url==None:
			url=self.new_url
		return urllib.parse.urlparse(url).path

#url=GEN_URL('10.204.29.221')
#print(url.get_url('/redfish/v2')

class GET_NODE(object):
	def __init__(self,host,app_ver, port):
		self.host=host
		self.url_list=[]
		self.app_ver=app_ver
		self.port=port
		self.url_obj=GEN_URL(host=self.host, rest_version=self.app_ver,port=self.port)

	def scan_node(self,node_path=None):
		"""
		node_path: str, get the root url if node_path is None
		"""
		node_url=self.url_obj.get_url(node_path)
		
		if CONF.REST.client_name in node_url:
			self.url_list.append(node_url)
			for sub_node_path in self.__get_sub_node(node_url):
				if sub_node_path != "":
					self.scan_node(sub_node_path)
		return self.url_list

	def __get_sub_node(self,node_url):
		url_request=URL_REQUEST(node_url)
		url_request.get_req()

		all_dict_got=[]
		all_dict_got=url_request.all_dict_in_response
		sub_node_path_list=[]
		if len(all_dict_got)>0:
			for sub_dict in all_dict_got:
				for key_conf in CONF.REST.subnode_keys:
					for key_host,value_host in sub_dict.items():
						if key_host == key_conf:
							if value_host not in sub_node_path_list and \
								self.url_obj.get_url(value_host) not in self.url_list:
								sub_node_path_list.append(value_host)
		#sub_node_path_list.remove(self.url_obj.get_path(node_url))
		return sub_node_path_list
		

class URL_REQUEST():

	def __init__(self,url,username=None, password=None):
		if CONF.REST.client_name not in url:
			raise ValueError("Not a valid redfish URL")
		self.response_dict={}
		self.all_dict_in_response={}
		self.url=url.strip().replace(" ", "%20")
		self.username=username
		self.password=password
		self.response_check=Reponse_check()

	@retry((HTTPError,socket.timeout,URLError,ValueError), 
			tries=CONF.REQUEST.retries, delay=CONF.REQUEST.delay,
			backoff=CONF.REQUEST.backoff, stoponerror=CONF.REQUEST.failonerror,
			logger=logger)
	def get_req(self,values=None):
		if values:
			if not isinstance(values,dict):
				raise TypeError("POST data should be a python dict")
			else:
				msg="POST: Attempting to request URL: {0}".format(self.url)
				data = urllib.parse.urlencode(values)
				data = data.encode('ascii') # data should be bytes
				req = urllib.request.Request(self.url, data)
		else:
			msg="GET: Attempting to request URL: {0}".format(self.url)
			req = urllib.request.Request(self.url)
		logger.info(msg)

		try:
			start_time=datetime.now()
			response = urllib.request.urlopen(req)
			#Need close the urlopen here??? or just run Burn-in
		except URLError as ue:
			if hasattr(ue,'reason'):
				msg='Failed to reach {1}:<hl> {0}</hl>.'.format(ue.reason,self.url)
				logger.error(msg)
			elif hasattr(ue,'code'):
				msg='The server couldn\'t fulfill the request. Error code: <hl>{0}</hl>'\
					.format(ue.code)
				logger.error(msg)
				if ue.code==401:
					self.Send_Auth()
			raise
		else:
			end_time=datetime.now()
			data=response.read().decode('utf-8')
			#To run Burn-in test, keep response.close() commented
			#response.close()

			request_time=(end_time-start_time).total_seconds()
			msg="Spent {0:6f}s to get response from {1:s}"\
				.format(request_time,self.url)
			logger.debug(msg)
			self.response_check.request_time_check(request_time,self.url)

		try:
			self.response_dict=json.loads(data)
			self.all_dict_in_response=json._default_decoder.all_dicts
		except ValueError as ve:
			msg="Get invaild feedback from RESTful server when open URL:{0}, \
				infor:<hl>{1}</hl>".format(self.url,data)
			logger.error(msg)
			raise
		#self.response_check.confcompare(self.response_dict,CONF.MAIN.value_file)
		self.response_check.confcompare(self.response_dict['Name'],\
					self.all_dict_in_response,CONF.MAIN.value_file)
		return self.response_dict

	def Send_Auth(self):
		if not (self.username and self.password):
			raise ValueError("Must specify both username and password, \
				as Server asks Authentication!")
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(None, self.url, self.username, self.password)
	
		authhandler = urllib.request.HTTPBasicAuthHandler(password_mgr)
		opener = urllib.request.build_opener(authhandler)
	#opener.open(url)
		urllib.request.install_opener(opener)

class Reponse_check(object):
	def __init__(self):
		pass
	def confcompare(self, current_url_name, all_dict_got, conf_file):
		if not os.path.isfile(conf_file):
			msg='Didn\'t find <hl>compare files</hl> to check the response data.'
			logger.error(msg)
		conf = configparser.ConfigParser()
		conf.optionxform = str
		conf.read(conf_file)
		if current_url_name in conf:
			for dict_got in all_dict_got:
				for key_got, value_get in dict_got.items():
					for check_item,check_spec in conf[current_url_name].items():
						if key_got==check_item:
							if "<" in check_spec:
								self.__threshold_check(current_url_name,check_item, check_spec, dict_got[check_item])
							else:
								if str(dict_got[check_item])==check_spec.strip():
									msg="{0}: Value mathced for key: {1}, got: {2}"\
										.format(current_url_name,check_item, check_spec.strip())
									logger.info(msg)
								else:
									msg="{0}: Value mismatched for key: <hl>{1}</hl>, expect: <hl>{2}</hl>, got: {3}"\
									.format(current_url_name,check_item, check_spec.strip(),str(dict_got[check_item]))
									logger.error(msg)
	
	def request_time_check(self, request_time,url):
		msg="RESTful Server takes <hl>'{0}'</hl> to respond URL:{1}".format(request_time,url)
		if request_time>CONF.REQUEST.http_time_warn and request_time<CONF.REQUEST.http_time_error:
			logger.warning(msg)
		elif request_time>CONF.REQUEST.http_time_error:
			logger.error(msg)

	def __threshold_check(self, current_url_name, key, threshold, value):
		thh=re.split('<',threshold)
		thh_n=[]
		i=0
		for th in thh:
			if 'x'==th.strip() or 'X'==th.strip():
				x=i
				thh_n.append(value)
			else:
				thh_n.append(ast.literal_eval(th.strip()))
			i+=1
	
		thh_n.sort()
		si=thh_n.index(value)
	
		offset=si-x
		if offset==0:
			msg="{0}: check {1} successfully, got: {2}"\
				.format(current_url_name,key, value)
			logger.info(msg)
		elif offset==1:
			msg="{0}: Warning, failed to check {1}, expect: {2}, got: <hl>{3}</hl>"\
				.format(current_url_name,key, threshold,value)
			logger.warning(msg)
		elif offset==2:
			msg="{0}: Error, failed to check {1}, expect: {2}, got: <hl>{3}</hl>"\
				.format(current_url_name,key, threshold,value)
			logger.error(msg)
		elif offset==-1:
			msg="{0}: Warning, failed to check {1}, expect: {2}, got: <hl>{3}</hl>"\
				.format(current_url_name,key, threshold,value)
			logger.warning(msg)
		elif offset==-2:
			msg="{0}: Error, failed to check {1}, expect: {2}, got: <hl>{3}</hl>"\
				.format(current_url_name,key, threshold,value)
			logger.error(msg)
