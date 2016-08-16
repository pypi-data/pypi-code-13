#! /usr/bin/env python

"""Unit test for footprint_archive.py"""

import footprint_archive
import unittest


goodCoordsList = ["09 42 35.13", "+58 51 04.6"]  # NGC 2950 (in DR2)
trickyCoordsList = ["12 31 59.34", "+14 25 13.4"]  # NGC 4501 (in DR5, but without sources)
badCoordsList = ["10 46 45.78", "-89 49 10.2"]    # outside SDSS

# NGC 2950:
goodReply1 = """
Begin FOOT on Sun Mar 30 08:32:38 CDT 2008
 at http://das.sdss.org/webscratch/FOOT/FOOT_18369_1206883958<p><title>SDSS Footprint Server: DR6 Results</title><h1> SDSS Footprint Server: DR6 Results</h1><p><a href="http://das.sdss.org/DR6-cgi-bin/FOOT?csvIn=ra%2Cdec%0D%0A145.646380%2C58.851280;inputFile=;do_bestBox=yes;Submit=Submit%20Request">Bookmark this link to recreate this query result</a></p><h4> <a href=http://das.sdss.org/webscratch/FOOT/FOOT_18369_1206883958/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://das.sdss.org/DR6-cgi-bin/ZIC?diameter=300&zoom=00&run=1345&rerun=41&camcol=3&field=234&rowc=915.13&colc=1566.19>145.646380,  58.851280, 1345,   41,    3,  234,   915.13,1566.19
</a></pre>Create a <a href=http://das.sdss.org/DR6-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request."""

# NGC 4501 (not in SDSS catalog, but observed):
goodReply2 = """
Begin FOOT on Sun Mar 30 08:47:20 CDT 2008
 at http://das.sdss.org/webscratch/FOOT/FOOT_24911_1206884840<p><title>SDSS Footprint Server: DR6 Results</title><h1> SDSS Footprint Server: DR6 Results</h1><p><a href="http://das.sdss.org/DR6-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=ra%2Cdec%0D%0A187.997250%2C14.420390;inputFile=;do_bestBox=yes">Bookmark this link to recreate this query result</a></p><h4> <a href=http://das.sdss.org/webscratch/FOOT/FOOT_24911_1206884840/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://das.sdss.org/DR6-cgi-bin/ZIC?diameter=300&zoom=00&run=4381&rerun=40&camcol=2&field=114&rowc=1012.99&colc=684.85>187.997250,  14.420390, 4381,   40,    2,  114,  1012.99, 684.85
</a></pre>Create a <a href=http://das.sdss.org/DR6-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request."""

noDataReply = """
Begin FOOT on Sun Mar 30 08:50:04 CDT 2008
 at http://das.sdss.org/webscratch/FOOT/FOOT_26055_1206885004<p><title>SDSS Footprint Server: DR6 Results</title><h1> SDSS Footprint Server: DR6 Results</h1><p><a href="http://das.sdss.org/DR6-cgi-bin/FOOT?Submit=Submit%20Request;csvIn=ra%2Cdec%0D%0A161.69075%2C-89.81950;inputFile=;do_bestBox=yes">Bookmark this link to recreate this query result</a></p><h4> <a href=http://das.sdss.org/webscratch/FOOT/FOOT_26055_1206885004/foot_best.csv>Best</a> version of Imaging (run/rerun/camcol/field)</h4><body bgcolor=#FFFFFF>
<pre>ra,        dec,       run,  rerun, camcol, field,  rowc, colc
<a href=http://das.sdss.org/DR6-cgi-bin/ZIC?diameter=300&zoom=00&run=0&rerun=0&camcol=0&field=0&rowc=0&colc=0>161.690750, -89.819500,    0,    0,    0,    0,     0,      0
</a></pre>Create a <a href=http://das.sdss.org/DR6-cgi-bin/FOOT>new request</a> or use your browser's back button to modify this request."""

noDataMessage = "No data found."
goodMessage = "Imaging data exists!\n\t\t(run, rerun, camcol, field = 1345 41 3 234)"



class FootprintArchiveTestCase(unittest.TestCase):
	def setUp(self):
		self.theArchive = footprint_archive.MakeArchive()


class MakeQuery(FootprintArchiveTestCase):
 	def testGoodQuery1(self):
		"""Live search: Do we get the correct HTML for NGC 2950?"""
		self.theArchive.InsertCoordinates(goodCoordsList)
 		textReceived = self.theArchive.QueryServer()
 		# strip off initial stuff which includes time of query and unique URLs
 		textReceived = textReceived.split("<pre>")[1]
 		goodReply = goodReply1.split("<pre>")[1]
		self.assertEqual(textReceived, goodReply)
 		
 	def testTrickyQuery(self):
		"""Live search: Do we get the correct HTML for NGC 4501?"""
		self.theArchive.InsertCoordinates(trickyCoordsList)
 		textReceived = self.theArchive.QueryServer()
 		# strip off initial stuff which includes time of query and unique URLs
 		textReceived = textReceived.split("<pre>")[1]
 		goodReply = goodReply2.split("<pre>")[1]
		self.assertEqual(textReceived, goodReply)
		
	def testBadQuery(self):
		"""Live search: Do we get the proper "no data" reply for coordinates outside SDSS?"""
		self.theArchive.InsertCoordinates(badCoordsList)
 		textReceived = self.theArchive.QueryServer()
 		# strip off initial stuff which includes time of query and unique URLs
 		textReceived = textReceived.split("<pre>")[1]
 		goodReply = noDataReply.split("<pre>")[1]
		self.assertEqual(textReceived, goodReply)

	def testAnalyzeHTML_GoodQuery(self):
		"""Does AnalyzeHTML respond properly to a good reply?"""
		self.theArchive.SetMode("fetchsdss")
		(messageString, nDataFound) = self.theArchive.AnalyzeHTML(goodReply1)
		self.assertEqual(messageString, goodMessage)

	def testAnalyzeHTML_BadQuery(self):
		"""Does AnalyzeHTML respond properly to a no-data reply?"""
		(messageString, nDataFound) = self.theArchive.AnalyzeHTML(noDataReply)
		self.assertEqual(messageString, noDataMessage)


if __name__	== "__main__":
	
	print "\n** Unit tests for footprint_archive.py **\n"
	unittest.main()	  
