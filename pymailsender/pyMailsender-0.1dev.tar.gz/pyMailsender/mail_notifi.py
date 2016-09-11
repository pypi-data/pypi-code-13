#!/usr/bin/python
import base64
import smtplib
import getpass
from operator import itemgetter
import math

ct = 0
a1 = {}
a2 = {}
a3 = {}
#TF-IDF
def doc_count(word):
	count = 0
	for i in a1:
		doc2 = []
		for word in a1[i]:
			word = word.lower()
			doc = [x.lower() for x in word.split(".") if len(x) > 1]
			for w in doc:
				doc2.append(w)
		if doc2.count(word) >= 1:
			count += 1
	return count

def tf(word, doc):
	return (doc.count(word)/float(len(doc)))

def idf(word):
	return math.log(ct/doc_count(word))

def tf_idf(word,doc):
	return (tf(word,doc)*idf(word))


def client_addr(client):
	global ct
	file1 = open("./mail_clients.txt")
	list1 = file1.read()
	i = 0
	for line in list1.split("\n"):
		l = len(line.split(" ")[0])
		a2[i] = line[(l+1):]
		line1 = line[0:l]
		line1 = line1.replace("-"," ")
		line1 = line1.replace("/"," ")
		line1 = line1.replace("("," ")
		line1 = line1.replace(")"," ")
		a1[i] = []
		for word in line1.split(" "):
			ct += 1
			a1[i].append(word)
		i += 1

	file1.close()


	for w in client.split(" "):
		w = w.lower()
		for i in a1:
			doc2 = []
			for word in a1[i]:
				word = word.lower()
				doc = [x.lower() for x in word.split(".") if len(x) > 1]
				for w1 in doc:
					doc2.append(w1)
			if i in a3:
				a3[i] += tf_idf(w,doc2)
			else:
				a3[i] = tf_idf(w,doc2)
			i += 1

def return_smtp_addr():
	 g = sorted(a3,key=a3.__getitem__,reverse=False)
	 i = g[0]
	 s = a2[i]
	 addr_list = []
	 for addr in s.split("|"):
	 	addr = addr.strip(" ")
	 	addr_list.append(addr)
	 return addr_list
				
def send(sender="",receiver="",subject="",text="",pwd=""):
	if sender == "":
		sender = raw_input("Enter Sender e-mail: ")
	if receiver == "":
		receiver = raw_input("Enter Receiver e-mail: ")
	if subject == "":
		subject = raw_input("Enter Subject: ")
	if text == "":
		text = raw_input("Enter Text: ")
	if pwd == "":
		pwd = getpass.getpass("Enter password: ")
	
	message = "From:" + sender + "To:" + receiver + "Subject:" + subject
	message += "\n"
	message += text
	
	client = raw_input("Enter your E-mail client: ")
	client_addr(client)
	smtp_addr = return_smtp_addr()
	flag = 0
	for addr in smtp_addr:
		if flag == 1:
			break
		try:
			smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
			smtpObj.starttls()
			smtpObj.login("hari.v91@gmail.com",pwd)
			smtpObj.sendmail(sender, receiver, message)
			smtpObj.quit()
			print "Successfully sent email"
			flag = 1
		except Exception,e:
			print e
			print "If the Error is on invalid E-mail client address, try giving a different name for the same"

if __name__ == '__main__':
    send()
