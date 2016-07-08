# -*- coding: utf-8 -*-


## System modules
import sys
import os
import csv

## import proteomics processing and graphics module
#from __future__ import print_functon
import pandas as pd
import GraphAssembly as asb
import GraphCalculation as calc
import ptm_processor as ptm



def ptm_batch_report(batch_file,project_directory):
    """
    This function will run the generate_report() function for each file in the batch. 
    The results will then be put into a report.
    
    arguments: 
        batch_file: file with the batch process information,
        project_directory: path to directory with project batch file and output results
    
    example:
        batch_file: should have 5 columns in csv file
            Path (path to search result file)	
            Pattern (pattern of the ptm search file name, when multiple fractions/sample)	
            Modification: (type of modification to be processed)
            ColumnName: (name of columns in output results file)
            Analysis_type: (type of search engine output and stringency criteria for filtering)
        project_directory: path to project directory     

    
    output:  
    """
    # Create batch file (BatchFile_PTM_input.csv)
    dataframe_container = []
    # Read the .csv batch file 
    os.chdir(project_directory)

    with open(batch_file, 'r') as csvfile:  ##py35
        new_line = csv.reader(csvfile)
        next(new_line, None)  # skip the headers
        # Loop throught the batch file and read the content of each folder
        for row in new_line:
            print(row)
            directory,file_pattern,modification,column_name,analysis_type = row[0],row[1],row[2],row[3],row[4]
			
            new_df = ptm.generate_report_input(directory,file_pattern,modification,analysis_type)
            new_df.columns = [column_name]
            dataframe_container.append(new_df)
	
    result = pd.concat(dataframe_container, axis = 1)
    os.chdir(project_directory)
    result.to_csv('batch_rep.csv')
    print("RESULT GENERATED")


def protein_graph(known_mod,unknown_mod,pep_interval,protein_length,filename):
    """ 
    Function to generate protein graphics from given input
    
    arguments: 
        known_mod (list of known modifications), 
        unknown_mod (list of unknown modifications),
        pep_interval (list of coordinates of identified peptides),
        protein_length (length of the protein),
        filename (file name to save SVG figure)
    
    example:
        known_mod = [50,100,125,195,400]
        unknown_mod = [75,110,125,295,600]
        pep_interval = [[1,20],[25,48],[15,55],[80,100],[25,48],[70,90],[400,600]]
        filename = 'test_pic2.svg'
        protein_length = 1500
    
    output:    
    """
    
    
    ## Test for the proteomics graphics package
    #known_mod = [50,100,125,195,400]
    #KnownMod = [75,110,125,295,600]
    #pep_interval = [[1,20],[25,48],[15,55],[80,100],[25,48],[70,90],[400,600]]
    #filename = test_pic.svg
    
    #Intialize graph and name the output file
    protein = asb.GraphAssemble(filename,protein_length)
	
    #Create the protein backbone
    protein.AddMolecule()
	
    #Add modificaton positions
    protein.AddTicks(known_mod,"circle")
    protein.AddTicks(unknown_mod,"triangle")
    
    #Calculate consensus peptide coverage
    pep_interval_unique = calc.calCulatePeptideCoverage(pep_interval)
    
    #Add peptide coverage to figure
    protein.AddCoverage(pep_interval_unique)
    
    #Print figure
    protein.PrintFigure()

    
def main():
    """
    Main entry point info the package
    
    
    """
        
    ## Test for the proteomics graphics package
    known_mod = [50,100,125,195,400]
    unknown_mod = [75,110,125,295,600]
    pep_interval = [[1,20],[25,48],[15,55],[80,100],[25,48],[70,90],[400,600]]
    filename = 'test_pic2.svg'
    protein_length = 1500
    
    # Generate protein graph
    #protein_graph(known_mod,unknown_mod,pep_interval,protein_length,filename)
    
    
    # Generate protein ptm reports
    batch_file = r'BatchFile_PTM_anaType_input.csv'
    project_directory = r'O:\Hanash_Lab_GPFS\Amin\LabDataProcessing\HaileyProjects\PythonProteomicsPipeline\package_testing'

    ptm_batch_report(batch_file,project_directory)


if __name__ == '__main__':
    sys.exit(main())