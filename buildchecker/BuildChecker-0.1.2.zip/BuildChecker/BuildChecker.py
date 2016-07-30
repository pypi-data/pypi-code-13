# -*- coding: utf-8 -*-
import smtplib
import logging
import datetime
import sys
import os
import time
import pdb
import atexit
import email.utils
from email.mime.text import MIMEText


class ClientConnect:
	def __init__(self,username,password,ph_no=None):
		"""
		args: username: email-id
			  password: email-id's password
			  ph_no:    Your phone Number with smsgateway ex: <ph_no>@mailmymobile.net for ultra Mobile
		visit http://www.thegeekstuff.com/2010/08/sms-using-email for getting sms gateway for your mobile.

		"""
		assert ((username is not None) and (password is not None)), "Please provide a valid username and password"

		self.username=str(username)
		self.password=str(password)
		self.start=datetime.datetime.now().minute
		self.ph_no=str(ph_no)
		self.body=None
		self.subject="**Info: Build Status **"
		if os.path.exists("filelog.log"):

			os.remove("filelog.log")
		self.connect()
		

	def connect(self):
		self.server=smtplib.SMTP("mail")
		

	def msgConstruct(self):
		self.msg=MIMEText(self.body)
		self.msg["To"]=email.utils.formataddr(("Recipient",self.username))
		self.msg["From"]=email.utils.formataddr(("BuildCenter",self.username))
		self.msg["Subject"]=self.subject
		

	def sendMail(self):
		try: 
			self.body_helper()
			self.msgConstruct()
			if self.ph_no is not None:

				self.server.sendmail(self.username,self.ph_no,self.msg.as_string())
			self.server.sendmail(self.username,self.username,self.msg.as_string())
			
		except:
			print "Message not able to send,Please check your credentials"
			

	def body_helper(self):

		with open("filelog.log","r") as f:

			body=f.read()
		if os.path.getsize("filelog.log")==0:
			self.subject="*** Info: Build Status ***"
			current_time=datetime.datetime.now().time()
			current_time=current_time.isoformat()
			if self.body is None:

				self.body="{} Program finished Successfully".format(current_time)
		else:
			self.body=body

	def startMonitor(self):
		logging.basicConfig(filename="filelog.log",filemode="w",format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",datefmt="%H:%M:%S",level=logging.DEBUG)
		def exception_hook(exc_type, exc_value, exc_traceback):
			
		    logging.error(
		        "Uncaught exception",
		        exc_info=(exc_type, exc_value, exc_traceback)
		    )
		    

		sys.excepthook = exception_hook
		
		def exit_handler():
			

			sys.excepthook=exception_hook
			self.sendMail()
		
		atexit.register(exit_handler)
	
	def progressCheck(self,**kwargs):
		

		st=""
		for i,v in kwargs.items():
			st+="{}: {}, ".format(i,v)
		self.body=st
		
		self.sendMail()

	




	


				


	






		



