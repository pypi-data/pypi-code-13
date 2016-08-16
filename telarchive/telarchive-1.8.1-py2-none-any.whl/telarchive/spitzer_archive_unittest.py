#! /usr/bin/env python

"""Unit test for spitzer_archive.py"""

import spitzer_archive
import unittest


#  Successful search (target was observed = NGC 2787 = 4 obs):
htmlFile = "html/Spitzer_n2787_result.html"
foundDataHTML = open(htmlFile).read()

#  Unsuccessful search (target not observed):
noData_htmlFile = "html/Spitzer_NoData.html"
foundNoDataHTML = open(noData_htmlFile).read()

ngc2787_coords = ["09 19 18.596", "+69 12 11.71"]




class SpitzerArchiveTestCase(unittest.TestCase):
	def setUp(self):
		self.theArchive = spitzer_archive.MakeArchive()	


class CheckAnalyzeHTML(SpitzerArchiveTestCase):
	def testNoDataFound(self):
		"""Check to see that case of "no data found" is correctly identified"""
		correctResult = ("No data found.", 0)
		result = self.theArchive.AnalyzeHTML(foundNoDataHTML)
		self.assertEqual(correctResult, result)
		
	def testDataExistsHTML(self):
		"""Analyzing HTML text indicating data exists"""
		correctResult = ('Data exists! (4 records found)', 4)
		result = self.theArchive.AnalyzeHTML( foundDataHTML )
		self.assertEqual(correctResult, result)
		
		

class MakeQuery(SpitzerArchiveTestCase):
	def setUp(self):
		self.theArchive = spitzer_archive.MakeArchive()	
		self.theArchive.InsertTarget("NGC 2787")
		self.theArchive.InsertBoxSize(1.0)
		print("MakeQuery.setUp: running live search for \"NGC 2787\"...")
		self.textReceived = self.theArchive.QueryServer()
		
	def testFindingData(self):
		"""Live search: Do we sucessfully find data for NGC 2787?"""
		correctResult = ('Data exists! (4 records found)', 4)
		result = self.theArchive.AnalyzeHTML(self.textReceived)
		self.assertEqual(correctResult, result)
		
	def testFindingDataByCoords(self):
		"""Live search: Do we find data for NGC 2787 using coords?"""
		self.theArchive.InsertTarget("")
		self.theArchive.InsertCoordinates(ngc2787_coords)
		correctResult = ('Data exists! (4 records found)', 4)
		print("MakeQuery.testFindingDataByCoords: running live search using coordinates for NGC 2787...")
		newText = self.theArchive.QueryServer()
		result = self.theArchive.AnalyzeHTML(newText)
		self.assertEqual(correctResult, result)
		




if __name__	== "__main__":
	
	print "\n** Unit tests for spitzer_archive.py **\n"
	unittest.main()	  
