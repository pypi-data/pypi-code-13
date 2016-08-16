# Archive class and module for SDSS Footprint-server archive
# 
# This module defines a new class (SDSSFootprintArchive) derived from the 
# BasicArchive class.
# 
#    This is meant to be used by fetchsdss.py (see below)
#    For Data Release 6 (DR6)
#       -- updated from DR4 version 2 Feb 2008
#       -- updated from DR3 version on 11 July 2005
#    
#    This has been modified from the "standard" SDSS archive class
# (sdss_archive.py) to permit more precise scanning of returned data,
# so as to extract the run, rerun, etc. info.  The latter data are
# included in the "message text" returned by AnalzyeHTML()

import re
import basic_archive
import utils

DEFAULT_TARGET = "No Target"
DEFAULT_BOXSIZE_STRING = "00 04 00"
MAX_ROWS_RETURNED = "1000"

DEFAULT_CSVCOORDS = "256.443154,58.0255"

# Sloan Digital Sky Survey, Data Release 6:
TARGET_LABEL = None
RA_LABEL = None
DEC_LABEL = None
RADEC_LABEL = "csvIn"
ARCHIVE_NAME = "Sloan Digital Sky Survey (DR6) Footprint Server"
ARCHIVE_SHORTNAME = "sdss-footprint"
ARCHIVE_URL ="http://das.sdss.org/DR6-cgi-bin/FOOT"
ARCHIVE_USER_URL = ARCHIVE_URL
DICT = {'Submit': "Submit Request", 'csvIn': DEFAULT_CSVCOORDS, 
		'inputFile': "", 'do_bestBox': "yes" }


#   Some regular expressions we will need:
#   Checks to see if the proxy server sent us a "no connection" message:
failedConnection = re.compile(r"The requested URL could not be retrieved")
#   Find "no data returned" equivalent for SDSS
findNoDataReturned = re.compile(r"""
	zoom=00&run=0&rerun=0&camcol=0&field=0&rowc=0&colc=0
	""", re.VERBOSE)
#   Check for data-returned reply and extract useful numbers
findPossibleData = re.compile(r"""
	zoom=00&run=(?P<run>\d+)&rerun=(?P<rerun>\d+)&camcol=(?P<camcol>\d+)&field=(?P<field>\d+)&
	""", re.VERBOSE)
# note that the desired fields can access thus:
#    m = findPossibleData.seach(someHTMLtext)
#    print m.group('run'), m.group('rerun'), m.group('camcol') et cetera


# Put all the functions in a list:
SEARCHES = []


# New class for SDSS searches:
class SDSSFootprintArchive( basic_archive.BasicArchive ):
	# No point in overriding the base class initialization for now
	
	def SetMode(self, mode_name):
		self.mode = mode_name
		
		
	def InsertBoxSize(self, box_size):
		# Useless for SDSS searches, so we do nothing
		pass


	def InsertTarget(self, target_name):
		# SDSS interface won't let us use target names, so we do nothing
		#    (in principle, we *could* do a coordinate lookup instead,
		#    but that's excessive)
		pass


	def InsertCoordinates(self, coords_list):
		# coords_list is a two-element list of strings; each string must
		# be in the usual "hh mm ss.s" format, though decimal values are optional.
		#    Overriden for SDSS searches, which require decimal degrees!
		ra_str = coords_list[0]
		dec_str = coords_list[1]
		# currently, we store RA & Dec in decimal degrees to an accuracy
		# of 0.1 arcsec
		# NOTE that there must be *no* space after the comma (search will silently
		# fail if there is a space)
		self.params[RADEC_LABEL] = "%.5f,%.5f" % utils.RADecToDecimalDeg(ra_str, dec_str)


	def AnalyzeHTML(self, htmlText, textSearches=None):
		#    Function which searches a big blob of HTML text.  We look for various
		# text fragments: signs of valid or invalid reply, did the archive find data
		# or not, etc.  Uses the regular-expression objects defined above.
		#    htmlText = big blob of HTML text (entire reply from archive, in a string)
		#    textSearches = not used here; listed for interface compatibility, since
		#                   archive_search.py will call this function with two
		#                   arguments
		
		# Default boolean flags:
		connectionMade = 1       # successfully connected to archive web server
		validReply = 0           # we got a genuine reply from the web server
		noDataExists = 0         # archive did proper search, found no data
		nDataFound = 0           # OUR flag indicating whether archive found data, and if so,
		                         #    how *many* data sets
	
		# Search the text, try to figure out if we got a valid result,
		# and if any data exists:
	
		# First, check to see if we got a well-formed reply (data or not):
		findData = findPossibleData.search(htmlText)
		# Now, check to see if there's any data present or not:
		if (findData):
			validReply = 1
			noDataExists = findNoDataReturned.search(htmlText)
			if (noDataExists):
				noDataExists = 1
				nDataFound = 0
			else:
				noDataExists = 0
				nDataFound = 1
	
		# Next, check to see if there was a screw-up of some kind.
		if ( failedConnection.search(htmlText) ):
			# Oops, couldn't connect to archive web server
			connectionMade = 0
			validReply = 0


		# Evaluate results of search and construct returned string:
		if ( connectionMade ):
			if ( validReply ):
				if ( nDataFound > 0 ):
					r = findData.group('run')
					rr = findData.group('rerun')
					cc = findData.group('camcol')
					f = findData.group('field')
# 					messageString = "Data: %s %s %s %s" % (r,rr,cc,f)
# 					messageString += " (run, rerun, camcol, field)"
					
					messageString = "Imaging data exists!"
					if (self.mode == "fetchsdss"):
						messageString += "\n\t\t(run, rerun, camcol, field ="
						messageString += " %s %s %s %s)" % (r,rr,cc,f)
				else:
					if ( noDataExists ):
						messageString = "No data found."
					else:
						messageString = "Strange reply from archive."
						nDataFound = -1
			else:
				messageString = "Invalid reply from archive (possibly malformed coordinates?)."
				nDataFound = -1
		else:
			messageString = "Failed connection to archive web site..."
			nDataFound = -1

		return (messageString, nDataFound)

# End Class



# Factory function to create an instance of SDSSFootprintArchive
def MakeArchive():
	return SDSSFootprintArchive(ARCHIVE_NAME, ARCHIVE_SHORTNAME, ARCHIVE_URL,
			DICT, SEARCHES, TARGET_LABEL, RA_LABEL, DEC_LABEL)



			

#  Here's what a successful search (target *was* observed) looks like (DR6):
foundDataHTML = """
Begin FOOT on Sat Feb  2 06:47:53 CST 2008
 at http://das.sdss.org/webscratch/FOOT/FOOT_6611_1201956473<p><title>SDSS Footprint Server: DR6 Results</title><h1> SDSS Footprint Server: DR6 Results</h1><p><a href="http://das.sdss.org/DR6-cgi-bin/FOOT?csvIn=187.996750%2C14.420417%0D%0A;inputFile=;do_bestBox=yes;Submit=Submit%20Request">Bookmark this link to recreate this query result</a></p><h4> <a href=http://das.sdss.org/webscratch/FOOT/FOOT_6611_1201956473/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://das.sdss.org/DR6-cgi-bin/ZIC?diameter=300&zoom=00&run=4381&rerun=40&camcol=2&field=114&rowc=1008.59&colc=685.04>187.996750,  14.420417, 4381,   40,    2,  114,  1008.59, 685.04
</a></pre>Create a <a href=http://das.sdss.org/DR6-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request.
"""

#  Here's what a successful search (target *was* observed) looks like (DR2):
foundDataHTML = """
Begin FOOT on Wed Jul 14 15:01:56 CDT 2004
 at http://sdsswww.fnal.gov/FOOT/FOOT_28216_1089835315<p><title>SDSS Footprint Server: DR2 Results</title><h1> SDSS Footprint Server: DR2 Results</h1><p><a href="http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=36.90558%2C-1.15647;inputFile=;do_bestBox=yes">Bookmark this link to recreate this query result</a></p><h4> <a href=http://sdsswww.fnal.gov/FOOT/FOOT_28216_1089835315/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://sdsswww.fnal.gov/DR2-cgi-bin/ZIC?diameter=300&zoom=00&run=3325&rerun=41&camcol=1&field=354&rowc=1088.85&colc=1045.01> 36.905580,  -1.156470, 3325,   41,    1,  354,  1088.85,1045.01
</a></pre>Create a <a href=http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request.
"""
#  And here's what an unsuccessful search (target not observed) looks like:
foundNoDataHTML = """
Begin FOOT on Wed Jul 14 15:04:43 CDT 2004
 at http://sdsswww.fnal.gov/FOOT/FOOT_28748_1089835483<p><title>SDSS Footprint Server: DR2 Results</title><h1> SDSS Footprint Server: DR2 Results</h1><p><a href="http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=28.305%2C4.19553;inputFile=;do_bestBox=yes">Bookmark this link to recreate this query result</a></p><h4> <a href=http://sdsswww.fnal.gov/FOOT/FOOT_28748_1089835483/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://sdsswww.fnal.gov/DR2-cgi-bin/ZIC?diameter=300&zoom=00&run=0&rerun=0&camcol=0&field=0&rowc=0&colc=0> 28.305000,   4.195530,    0,    0,    0,    0,     0,      0
</a></pre>Create a <a href=http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request.
"""
# And here's the reply to an empty or malformed query:
badQueryHTML = """
Begin FOOT on Wed Jul 14 14:59:14 CDT 2004
 at http://sdsswww.fnal.gov/FOOT/FOOT_27816_1089835153<p><title>SDSS Footprint Server: DR2 Results</title><h1> SDSS Footprint Server: DR2 Results</h1><p><a href="http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=;inputFile=;do_bestBox=yes">Bookmark this link to recreate this query result</a></p><h4> <a href=http://sdsswww.fnal.gov/FOOT/FOOT_27816_1089835153/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
</pre>Create a <a href=http://sdsswww.fnal.gov/DR2-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request.
"""