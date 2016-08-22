#!/usr/bin/python3
# coding=utf-8
# -*- encoding: utf-8 -*-

import json, sys, re, xml, os, hashlib, string
import subprocess
from apertium_lint import bidix_lint
from apertium_lint import transfer_lint
from apertium_lint import modes_lint
from apertium_lint import tagger_lint

def readConfig():
	try:
		config = open('config.json')

		try:
			json.load(config)
		except ValueError:
			print("Error : 	Config file does not contain valid JSON")
			print("Please validate and try again")
			exit(1)

	except FileNotFoundError:
		print("File not found : config.json not found in present directory")
		print("Please use a valid config file and try again")
		exit(1)

	print("Valid config.json loaded succesfully")

def parseFile(fName, fPath):
	"""
	Given the filename determines what
	kind file we are working with.
	"""

	#Dictionaries
	for x in range(2):
		for y in range(2):

			match = re.search("apertium-[a-z]{"+ str(x+2)+ "}-[a-z]{"+ str(y+2)+ "}\.[a-z]{"+ str(y+2)+ "}\.dix", fName)
			if match != None and os.path.isfile(fPath):
				print("Working with monodix : "+ fName)
				return "monodix"

			match = re.search("apertium-[a-z]{"+ str(x+2)+"}\.[a-z]{"+ str(y+2)+ "}\.dix", fName)
			if match != None and os.path.isfile(fPath):
				print("Working with monodix : "+ fName)
				return "monodix"

			match = re.search("apertium-[a-z]{"+ str(x+2)+ "}-[a-z]{"+ str(y+2)+ "}\.[a-z]{"+ str(x+2)+ "}-[a-z]{"+ str(y+2)+ "}\.dix", fName)
			if match != None and os.path.isfile(fPath):
				print("Working with bidix : "+ fName)
				return "bidix"

	#Transfer files
	match = re.search("apertium.*\.t[0-3]x", fName)
	if match != None and os.path.isfile(fPath):
		print("Working with transfer file : "+ fName)
		return "transfer"

	#Modes files
	match = re.search("modes.xml", fName)
	if match != None and os.path.isfile(fPath):
		print("Working with modes file : "+ fName)
		return "modes"

	#Tagger files
	match = re.search("apertium.*\.tsx", fName)
	if match != None and os.path.isfile(fPath):
		print("Working with tagger file : "+ fName)
		return "tagger"

	print("Invalid file")
	exit(1)

def main():

	if len(sys.argv) != 2:
		print ("Error : Invalid number of arguments")
		print ("To run : python3 <filename>")
		exit(1)

	categories = {"monodix":"dict_lint", "bidix":"bidix_lint", "transfer":"transfer_lint", "modes":"modes_lint", "tagger":"tagger_lint"}
	fName = sys.argv[1]
	fName = fName.strip()
	fType = parseFile(fName.split('/')[-1], fName)
	readConfig()

	if fType == 'monodix':
		dict_lint.main(fName)

	elif fType == 'bidix':
		bidix_lint.main(fName)

	elif fType == 'transfer':
		transfer_lint.main(fName)
	
	elif fType == 'modes':
		modes_lint.main(fName)

	elif fType == 'tagger':
		tagger_lint.main(fName)
		
	else :
		print("Support coming in soon")

	#Can do a subprocess call here or work on the individual files


if __name__ == '__main__':
	main()
