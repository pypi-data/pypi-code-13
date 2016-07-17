#!/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import sys
import codecs
import os


reserved = [(" and ", " && "),  (" or ", " || "),  (" is not ", " !== "),  (" is ", " === "),  (" not like ", " != "),  (" like ", " == "),  (" not ", " !"),  (" unlike ", " != "),  ("None", "null"),  ("except", "catch"),  ("def", "function"),  ("#", "//")]

abc = "abcdefghijklmnopqrstuvwxyz"

def randomVariableName():
	varname = ""
	for x in range(20):
		varname = varname + random.choice(abc)
	return varname

def tag_code(s):
	code = []
	is_string = False
	string_char = ''
	escaped = False
	current_block = ""
	for c in s:
		if is_string:
			if not escaped and c == string_char:
				code.append((current_block + c, "string"))
				current_block = ""
				is_string = False
				continue
			elif escaped:
				escaped = False
			elif c == "\\":
				escaped = True
			current_block = current_block +c
		else:
			if c == "\"":
				string_char = "\""
				code.append((current_block, "code"))
				current_block = "\""
				is_string = True
			elif c == "\'":
				string_char = "\'"
				code.append((current_block, "code"))
				current_block = "\'"
				is_string = True
			else:
				current_block = current_block +c
	code.append((current_block, "code"))
	return code

def replace_reserved_words(s_line):
	tags = tag_code(s_line)
	code_s = ""
	for tag in tags:
		text = tag[0]
		if tag[1] == "code":
			for rese in reserved:
				text = text.replace(rese[0], rese[1])
		code_s = code_s + text
	return code_s


def compile_js(mscript):
	javascript = "//This file has been automatically compiled from MScript source\n\n";
	isComment = False;
	for line in mscript:
		line = line.replace("\t", " ").replace("\n", "").replace("\r", "")
		line = line.strip()
		if not isComment:
			#Previous line is not a comment, let's roll!
			if line.startswith("/*"):
				#...But this line started a comment block :-(
				isComment = True
			elif line == "":
				#Empty line
				continue
			else:
				#Time to change reserved words like "is", "like", "not" to JS ones
				line = replace_reserved_words(line)
				#Then we'll change loops and such
				replaceEnding = "){"
				if line.startswith("if "):
					line = "if (" + line[2:]
				elif line.startswith("try ") or line.startswith("try:"):
					line = "try {"
					replaceEnding = ""
				elif line.startswith("else if "):
					line = "else if (" + line[7:]
				elif line.startswith("else ") or line.startswith("else:"):
					line = "else {"
					replaceEnding = ""
				elif line == "end":
					line = "}";
					replaceEnding = "";
				elif line.startswith("while "):
					line = "while (" + line[5:]
				elif line.startswith("for "):
					variable = randomVariableName()
					if line.endswith(":"):
						line = line[0:-1]
					elif line.endswith(" then"):
						line = line[0:-4]
					line = line[3:]
					index = line.index(" in ")
					var1 = line[0:index]
					var2 = line[index+4:]
					line = "for (var " + variable + " = 0;" + variable + "<" + var2 + ".length; " + variable + "++){\n" + "var " + var1 + " = " + var2 + "[" + variable + "];"
					replaceEnding = ""
				elif line.startswith("forr "):
					variable = randomVariableName()
					if line.endswith(":"):
						line = line[0:-1]
					elif line.endswith(" then"):
						line = line[0:-4]
					line = line[4:]
					index = line.index(" in ")
					var1 = line[0:index]
					var2 = line[index+4:]
					line = "for (var " + variable + " = " + var2 + ".length-1; " + variable + ">=0;" + variable + "--){\n" + "var " + var1 + " = " + var2 + "[" + variable + "];"
					replaceEnding = ""
				elif line.startswith("foreach "):
					line = "for ( var " + line[7:]
				elif line.startswith("catch "):
					line = "for ( var " + line[5:]
				elif line.startswith("finally ") or line.startswith("finally:"):
					line = "finally ("
					replaceEnding = ""
				elif line.startswith("print "):
					line = "console.log(" + line[5:]
					replaceEnding = ");"
				elif line.startswith("class "):
					if "(" in line:
						#extends
						line = line.replace("(", " extends ")
						line = line.replace(")", "")
				else:
					if not line.endswith(":") and not line.endswith(" then"):
						replaceEnding = ""
						line = line + ";"
					elif "function" in line:
						replaceEnding = "{"

				if len(replaceEnding) != 0:
					if line.endswith(":"):
						line = line[0: -1] + replaceEnding
					elif line.endswith(" then"):
						line = line[0: -4] + replaceEnding
					else:
						line = line + replaceEnding
		else:
			#Previous line was part of a comment block, and so is this one
			if line.endswith("*/"):
				#This is the last line of the comment block
				isComment = False

		javascript = javascript + line + "\n"

	return javascript

def save_js_library(location):
	js_path = os.path.dirname(os.path.realpath(__file__))
	js_file = os.path.join(js_path, "mslib.js")
	orig_file = codecs.open(js_file, "r", "utf-8")
	new_file = codecs.open(location, "w", "utf-8")
	new_file.write(orig_file.read())
	orig_file.close()
	new_file.close()

def main():
	args = sys.argv
	if len(args) < 2:
		print("Please specify an mscript file!")
		print("usage: mscript /path/to/input.mscript  ( /path/to/output.js )")
		print("to get the library use: mscript -lib /path/where/to/copy/the_library.js")
		sys.exit(1)

	mscript_path = args[1]
	if mscript_path == "-lib":
		if len(args) != 3:
			print("mscript -lib takes exactyl one argument, ", len(args)-2, " given!")
			sys.exit(1)
		else:
			save_js_library(args[2])
			sys.exit(0)
	if len(args) == 2:
		if mscript_path.endswith(".mscript"):
			js_path = mscript_path[:-8] + ".js"
		else:
			js_path = mscript_path + ".js"
	else:
		js_path = args[2]

	mscript_file = codecs.open(mscript_path, "r", "utf-8")
	js = compile_js(mscript_file)
	mscript_file.close()
	output = codecs.open(js_path, "w", "utf-8")
	output.write(js)
	output.close()
	sys.exit(0)

def mscript_to_javascript(mscript_text):
	script = mscript_text.split("\n")
	return compile_js(script)


if __name__ == "__main__":
	main()
