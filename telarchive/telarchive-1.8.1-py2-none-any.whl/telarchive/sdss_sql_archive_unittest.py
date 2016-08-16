#! /usr/bin/env python

"""Unit test for sdss_sql_archive.py"""

import sdss_sql_archive
import unittest


goodCoordsList1 = ["09 42 35.26", "+58 51 03.9"]  # NGC 2950 (in DR2)
goodCoordsList2 = ["12 24 55.53", "+11 42 14.1"]  # NGC 4371 (in DR4)
badCoordsList = ["10 46 45.78", "-89 49 10.2"]    # outside SDSS

goodReply1 = "run,rerun,camcol,field\n1345,41,3,234\n"  # NGC 2950
goodMessage = "Imaging data exists!\n\t\t(run, rerun, camcol, field = 1345 41 3 234)"

goodReply2 = "run,rerun,camcol,field\n3804,41,2,190\n"  # NGC 4371

noDataReply = "No objects have been found"
noDataMessage = "No data found."



class SloanArchiveTestCase(unittest.TestCase):
	def setUp(self):
		self.theArchive = sdss_sql_archive.MakeArchive()


class MakeQuery(SloanArchiveTestCase):
 	def testGoodQuery1(self):
		"""Live search: Do we sucessfully find NGC 2950 (DR2)?"""
		self.theArchive.InsertCoordinates(goodCoordsList1)
 		textReceived = self.theArchive.QueryServer()
		self.assertEqual(textReceived, goodReply1)
		
 	def testGoodQuery2(self):
		"""Live search: Do we sucessfully find NGC 4371 (DR4)?"""
		self.theArchive.InsertCoordinates(goodCoordsList2)
 		textReceived = self.theArchive.QueryServer()
		self.assertEqual(textReceived, goodReply2)
		
	def testBadQuery(self):
		"""Live search: Do we get the proper "no data" reply for coordinates outside SDSS?"""
		self.theArchive.InsertCoordinates(badCoordsList)
 		textReceived = self.theArchive.QueryServer()
		self.assertEqual(textReceived, noDataReply)

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
	
	print "\n** Unit tests for sdss_sql_archive.py **\n"
	unittest.main()	  
