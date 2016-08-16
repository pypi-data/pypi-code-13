#! /usr/bin/env python

"""Unit test for ukirt_archive.py"""

import ukirt_archive
import unittest


ngc4321_coordsList = ["12 22 54.95", "+15 49 19.5"]
#  Successful search (target was observed = NGC 4321 w/ 4.0 arcmin box = 77 obs):
htmlFile = "html/ngc_4321_ukirt.csv"
foundDataCSV = open(htmlFile).read()
nDataFoundCorrect = 58

#  Unsuccessful search (target not observed):
htmlFile = "html/ukirt_nodata.csv"
foundNoDataHTML = open(htmlFile).read()

#  Bad object name:
#htmlFile = "ngc_bob_ing.html"
#badQueryHTML = open(htmlFile).read()



class UKIRTArchiveTestCase(unittest.TestCase):
	def setUp(self):
		self.theArchive = ukirt_archive.MakeArchive()


class CheckAnalyzeHTML(UKIRTArchiveTestCase):
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


class MakeQuery(UKIRTArchiveTestCase):
	def setUp(self):
		self.theArchive = ukirt_archive.MakeArchive()	
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
 		correctInstCount = "\n\t\tUFTI (58)"
 		instCount = self.theArchive.DoSpecialSearches(self.textReceived, 1)
 		self.assertEqual(correctInstCount, instCount)


if __name__	== "__main__":
	
	print "\n** Unit tests for ukirt_archive.py **\n"
	unittest.main()	  
