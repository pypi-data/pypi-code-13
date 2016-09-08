#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
class send_gmail(object):
	@staticmethod
	def error_out():
		err_mssg = '[err] account, passwd, subject, msg_to parameters should be NOT empty.'
		print(err_mssg)
		exit(0)
	@staticmethod
	def doIt(account='', passwd='', body='', subject='', msg_to='', msg_from=''):
		if account is None or len(account)<1: send_gmail.error_out()
		if passwd is None or len(passwd)<1: send_gmail.error_out()
		if subject is None or len(subject)<1: send_gmail.error_out()
		if msg_to is None or len(msg_to)<1: send_gmail.error_out()
		msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = account if msg_from=='' else msg_from
		msg['To'] = msg_to
		conn = smtplib.SMTP('smtp.gmail.com', 587)
		conn.ehlo()
		conn.starttls()
		conn.ehlo()
		conn.login(account, passwd)
		conn.send_message(msg)
		conn.close()
