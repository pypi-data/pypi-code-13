#!/usr/bin/env python
'''
Author: Joseph P. Murphy
Date: 08/10/2016

This file is part of Simple-Passgen.

Simple-Passgen is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Simple-Passgen is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Simple-Passgen.  If not, see <http://www.gnu.org/licenses/>.

'''
import sys,os,math
def main():
	exit_status = 0
	try:
		s = ''
		i = 10
		if len(sys.argv) > 1:
			try:	
				i = int(sys.argv[1])
			except ValueError:
				raise ValueError('Argument error: please enter a valid integer for password length argument')
		if i < 8:
			print 'Warning: using less than 8 characters is not recommended and will lead to a less secure password.  Please use a recommended 8-12 character password length for more security.'
		elif i >= 8 and i < 10:
			print 'Password grade: moderate'
		elif i >= 10 and i < 13:
			print 'Password grade: strong'
		else:
			print 'Password grade: extremely strong'
		bytes = math.log(94, 2) * i
		combos = math.pow(94, i)
		print 'Approx. Bytes of Entropy: ' + str(bytes)
		print 'Number of possible combinations:  ' + str(combos)
		for x in range(0,i):
			n = (int(((float(int(os.urandom(1).encode('hex'),16)))/255)*94))+33
			if n > 126:
				raise ValueError('Out of Bounds Error: please discontinue use of this script as it is misbehaving.')
			s = s + str(unichr(n))
		print 'Password:  ' + s
	except SystemExit as exc:
        	exit_status = exc.code

    	return exit_status
if __name__ == "__main__":
    main()
