#! /usr/bin/env python

"""Unit test for cfht_archive.py"""

import cfht_archive
import unittest


ngc4321_coordsList = ["12 22 54.95", "+15 49 19.5"]
#  Successful search (target was observed = NGC 4321 w/ 4.0 arcmin box = 77 obs):
htmlFile = "html/ngc_4321_cfht.csv"
foundDataCSV = open(htmlFile).read()
nDataFoundCorrect = 235

#  Unsuccessful search (target not observed):
htmlFile = "html/cfht_nodata.csv"
foundNoDataHTML = open(htmlFile).read()

#  Bad object name:
#htmlFile = "ngc_bob_ing.html"
#badQueryHTML = open(htmlFile).read()



class CFHTArchiveTestCase( unittest.TestCase ):
	def setUp(self):
		self.theArchive = cfht_archive.MakeArchive()


class CheckAnalyzeHTML( CFHTArchiveTestCase ):
 	def testDataExistsHTML( self ):
 		"""Analyzing HTML text indicating data exists"""
 		correctResult = ("Data exists! (%d observations found)" % nDataFoundCorrect, nDataFoundCorrect)
 		result = self.theArchive.AnalyzeHTML( foundDataCSV )
 		self.assertEqual(correctResult, result)
		
	def testNoDataHTML(self):
		"""Analyzing HTML text indicating no data exists"""
		correctResult = ("No data found.", 0)
		result = self.theArchive.AnalyzeHTML( foundNoDataHTML )
		self.assertEqual(correctResult, result)


class MakeQuery(CFHTArchiveTestCase):
	def setUp(self):
		self.theArchive = cfht_archive.MakeArchive()	
		self.theArchive.InsertCoordinates(ngc4321_coordsList)
		self.theArchive.InsertBoxSize(4.0)
		print("MakeQuery.setUp: running live search using coords for NGC 4321...")
		self.textReceived = self.theArchive.QueryServer()
		
	def testFindingData(self):
		"""Live search: Do we sucessfully find data for NGC 4321?"""
 		correctResult = ("Data exists! (%d observations found)" % nDataFoundCorrect, nDataFoundCorrect)
		result = self.theArchive.AnalyzeHTML(self.textReceived)
		self.assertEqual(correctResult, result)
		
 	def testCountingData(self):
 		"""Live search: Do we find and count instruments for NGC 4321?"""
 		correctInstCount = "\n\t\tHRCAM (46), MegaPrime (189)"
 		instCount = self.theArchive.DoSpecialSearches(self.textReceived, 1)
 		self.assertEqual(correctInstCount, instCount)


if __name__	== "__main__":
	
	print "\n** Unit tests for cfht_archive.py **\n"
	unittest.main()	  
