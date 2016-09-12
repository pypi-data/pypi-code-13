#!/usr/bin/env python
# -*- coding: utf-8 -*-

# colorecho: Wraps your strings in terminal color codes.
# The same code should work in python2.7 & python3.x.

# MIT License

# Copyright (c) 2016 Mahyar McDonald

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys

class TerminalColorizer(object):
	"Wraps your strings in terminal color codes."

	rootEscape = "\x1b[%sm"
	resetSymbol = "\x1b[0m"

	two56ForegroundColorEscapeCodes = [38,5]
	two56BackgroundColorEscapeCodes = [48,5]

	basicModifiers = {
		"bold" : 1,
		"dim" : 2,
		"italic" : 3, #not widely supported
		"underlined" : 4,
		"blink" : 5,
		"invert" : 7,
		"hidden" : 8,
		"strikeout" : 9, #not widely supported
	}

	basicForegroundColors = {
		"default":39,
		"black":30,
		"red":31,
		"green":32,
		"yellow":33,
		"blue":34,
		"magenta":35,
		"cyan":36,
		"light-gray":37,
		"dark-gray":90,
		"light-red":91,
		"light-green":92,
		"light-yellow":93,
		"light-blue":94,
		"light-magenta":95,
		"light-cyan":96,
		"white":97,
	}

	basicBackgroundColors = {
		"default" : 49,
		"black" : 40,
		"red" : 41,
		"green" : 42,
		"yellow" : 43,
		"blue" : 44,
		"magenta" : 45,
		"cyan" : 46,
		"light-gray" : 47,
		"dark-gray" : 100,
		"light-red" : 101,
		"light-green" : 102,
		"light-yellow" : 103,
		"light-blue" : 104,
		"light-magenta" : 105,
		"light-cyan" : 106,
		"white" : 107 ,
	}

	def digitCheck(self,arg,digitCodes,nameCodes):
		if arg != None and arg.isdigit():
			if 1 <= int(arg) <= 256:
				return digitCodes+[arg]
			else:
				return [None]
		else:
			return [nameCodes.get(arg)]

	def makeSymbol(self,foregroundColor,backgroundColor,modifier):
		foreground = self.digitCheck(foregroundColor, self.two56ForegroundColorEscapeCodes, self.basicForegroundColors)
		background = self.digitCheck(backgroundColor, self.two56BackgroundColorEscapeCodes, self.basicBackgroundColors)
		modifier = [self.basicModifiers.get(modifier)]

		codes = foreground + background + modifier
		codes = [str(x) for x in codes if x is not None] #filter out None types, convert to strings
		return self.rootEscape % ";".join(codes)

	def makeString(self,foregroundColor,backgroundColor,modifier,string):
		symbol = self.makeSymbol(foregroundColor,backgroundColor,modifier)
		return symbol + string + self.resetSymbol


class CommandLineUI(object):
	"Takes command line input and prints a colorized string."

	def setupArgs(self,color):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)

		description = """Prints terminal \x1b[32mcolorized\x1b[0m versions of your strings.  For example:

$ {0} red "Hello fine sir"
\x1b[31mHello fine sir\x1b[0m
$ {0} -b 180 -m blink 1 "Hello fine sir"
\x1b[38;5;1;48;5;180;5mHello fine sir\x1b[0m
$ {0} --raw -b 180 -m blink red Hello fine sir
'\\x1b[31;48;5;180;5mHello fine sir\\x1b[0m' 
$ cowsay Hello fine sir | {0} -m blink green 
<A blinking green cow who says: "Hello fine sir">""".format(parser.prog)

		parser.description = description

		parser.add_argument('-r','--raw',action='store_true',
			help="Print raw version of the color string.")
		parser.add_argument('-b','--background_color',
			help="Set a background color for your text. You can put a number between 0..256 if your terminal supports it or choose from these names: " + ', '.join(color.basicBackgroundColors.keys()))
		parser.add_argument('-m','--modifier',
			help="Set a modifier for your text. Choose from these names: " + ', '.join(color.basicModifiers.keys()) + '. Italic and strikeout is not widely supported in terminals.' )
		parser.add_argument('colorName',
			help="The name of the color you want.  You can put a number between 0..256 if your terminal supports it or choose from these names: " + ', '.join(color.basicForegroundColors.keys()))
		parser.add_argument('string', default=[], nargs='*', help="Whatever text you want to colorize.")

		return parser.parse_args()

	def colorString(self,color,args,string):
		outputString = color.makeString(args.colorName, args.background_color, args.modifier, string)

		if args.raw:
			outputString = repr(outputString)

		sys.stdout.write(outputString)

	def execute(self):
		color = TerminalColorizer()
		args = self.setupArgs(color)
		string = " ".join(args.string)

		if string:
			self.colorString(color,args,string+"\n")
		else:  # nothing specified in the command line args, so do read stdin mode
			for line in sys.stdin:
				self.colorString(color,args,line)


if __name__ == "__main__":
    CommandLineUI().execute()

