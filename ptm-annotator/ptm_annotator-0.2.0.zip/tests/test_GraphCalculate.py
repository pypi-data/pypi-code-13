# -*- coding: utf-8 -*-

#from __future__ import print_functon
import GraphAssembly as asb
import GraphCalculation as calc
import sys


def main():
    """ Main entry point for the script.
    """
    
    
    ## Test for the proteomics graphics package
    KnownMut = [50,100,125,195,400]
    KnownMod = [75,110,125,295,600]
    PepInterval = [[1,20],[25,48],[15,55],[80,100],[25,48],[70,90],[400,600]]
    
	#Name the output file
    protein = asb.GraphAssemble("test_1125.svg")
	
	#Create the protein backbone
    protein.AddMolecule()
	
	#Add modificaton positions
    protein.AddTicks(KnownMut,"circle")
    protein.AddTicks(KnownMod,"triangle")
    
	#Calculate consensus peptide coverage
    pep_interval_unique = calc.calCulatePeptideCoverage(PepInterval)
    
	#Add peptide coverage to figure
    protein.AddCoverage(pep_interval_unique)
	
	#Print figure
    protein.PrintFigure()

if __name__ == '__main__':
    sys.exit(main())

import GraphAssembly as asb
import GraphCalculation as calc


def test_calCulatePeptideCoverage(PepInterval):
	""" Tests the return of consesnsus peptide coverage from individul peptides
	"""
	
	PepInterval = [[1,20],[25,48],[15,55],[80,100],[25,48],[70,90],[400,600]]
	
	assert calc.calCulatePeptideCoverage(PepInterval) == 

