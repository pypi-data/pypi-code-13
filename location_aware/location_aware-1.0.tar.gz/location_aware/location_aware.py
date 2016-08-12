#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2014 Robert Dam (Concept, algorithms and ruby code)
# Copyright (c) 2016 Javier Gonzalez (Python code and library)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#------------------------------------------------------------------------------

one = "DGJKLMNRST"
lpos = []
lneg = []
latlonms = []

def location_aware_init():
	global lpos, lneg, latlonms
	abc = "ABCDEFGIJKLMNOPRSTUVXZ"
	vowels = "AEIOU"
	consonants = "BCDFGJKLMNPRSTZ"
	latlon = []
	for v1 in vowels:
		for v2 in vowels:
			for x in abc:
				if x not in vowels:
					latlon.append(v1+x+v2)
	for i in range(0,181):
		lpos.append(latlon[2*i])
		lneg.append(latlon[2*i+1])
	for c1 in consonants:
		for v in vowels:
			for c2 in consonants:
				latlonms.append(c1+v+c2)

def part_encode(l_str, modstr):
	spl = str(float(l_str)).split(".")
	integ = abs(int(spl[0]))
	if modstr == 'latitude':
		assert integ <= 90
	else:
		assert integ <= 180
	if l_str.startswith("-"):
		linteg = lneg[integ]
	else:
		linteg = lpos[integ]
	dec = abs(int(spl[1][0:6]))
	ldec = len(str(dec))
	if ldec == 1:
		return one[dec] + linteg
	elif ldec == 2:
		return latlonms[dec*10] + linteg
	elif ldec == 3:
		return latlonms[dec] + linteg
	elif ldec == 4:
		return latlonms[int(str(dec)[0:3])] + linteg + one[int(str(dec)[3])]
	elif ldec == 5:
		return latlonms[int(str(dec)[0:3])] + linteg + latlonms[int(str(dec)[3:6])*10]
	elif ldec == 6:
		return latlonms[int(str(dec)[0:3])] + linteg + latlonms[int(str(dec)[3:6])]

def part_decode(l_str, modstr):
	def one_index(elem):
		assert elem in one
		return str(one.index(elem))
	def latlonms_index(elem):
		assert elem in latlonms
		return "{0:03d}".format(latlonms.index(elem))
	def latlon_index(elem, modstr):
		if modstr == 'latitude':
			limit = 90
		else:
			limit = 180
		if elem in lpos:
			ret = lpos.index(elem)
			assert ret <= limit
			return str(ret)
		else:
			assert elem in lneg
			ret = lneg.index(elem)
			assert ret <= limit
			return "-"+str(ret)
	llstr = len(l_str)
	assert llstr in [4,6,7,9]
	if llstr == 4:
		return float(latlon_index(l_str[1:4], modstr) +"."+ one_index(l_str[0]))
	elif llstr == 6:
		return float(latlon_index(l_str[3:6], modstr) +"."+ latlonms_index(l_str[0:3]))
	elif llstr == 7:
		return float(latlon_index(l_str[3:6], modstr) +"."+ latlonms_index(l_str[0:3]) + one_index(l_str[6]))
	elif llstr == 9:
		return float(latlon_index(l_str[3:6], modstr) +"."+ latlonms_index(l_str[0:3]) + latlonms_index(l_str[6:9]))

def encode(lat, lon):
	"""Encode *latitude* and *longitude* coordinates into its location_aware address"""
	return part_encode(str(lat), 'latitude') +"-"+ part_encode(str(lon), 'longitude')

def decode(location_aware_name):
	"""Decode a *location_aware_name* like 'DEXA-DASA' or 'RERI-NUCA' into it's latitude and longitude coordinates"""
	spl = location_aware_name.split("-")
	assert len(spl) == 2
	return part_decode(spl[0], 'latitude'), part_decode(spl[1], 'longitude')
