#Amin Momin/Hailey Haut

#Thermo peptide_psms file converter

from Bio.Seq import Seq
import gzip
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import pickle
import sys
import glob
from Bio import SeqIO

def parse_uniprot_header(header):
	'''A function that parse through an individual proteome reference fasta record
	downloaded from Uniprot.
	
	Arguments: 
	input header line from individual fasta record.
	output: string printed with ac, entry, db
	Input:
	>sp|A0A023GPJ0|CDII_ENTCC Immunity protein CdiI OS=Enterobacter cloacae subsp.
	cloacae (strain ATCC 13047 / DSM 30054 / NBRC 13535 / NCDC 279-56) GN=cdiI PE=1 SV=2
	
	Output:
	>A0A023GPJ0 sp|A0A023GPJ0|CDII_ENTCC Immunity protein CdiI OS=Enterobacter cloacae subsp.
	cloacae (strain ATCC 13047 / DSM 30054 / NBRC 13535 / NCDC 279-56) GN=cdiI PE=1 SV=2
	'''
	
    ## Parse and extract db(sp/tr), Uniprot accession number (A0A024R161,) 
    ## and Uniprot entry (A0A024R161_HUMAN) from the line
    #header_id = header.split(' ')
	header = re.sub('^>','',header)
	n = re.search(r"(\w+)\|([a-zA-Z0-9\-]+)\|(\w+)\s", header)
	db,ac,entry = 'sp','Undefined','No_species'
	if n:
		db = n.group(1)
		ac = n.group(2)
		entry = n.group(3)
      header_newformat = '>'+ac+' '+header
      return (header_newformat)

	
	
def format_uniprotFasta(file_directory,input_file_name,output_file_name):
	'''
	Convert Fasta header line to list the Uniprot accesstion before the description
	
	Argument:
	file_directory -- location of the fasta sequence file downloaded from Uniprot; eg 'O:\Hanash_Lab_GPFS\Amin\Database\Uniprot_2013'
	input_file_name -- name of fasta file to be formated; eg 'HUMAN_March_2013.fasta'
	output_file_name -- name of formated fasta file; eg 'HUMAN_March_2013_protgraphic_format.fasta'
	
	Example input:
	>sp|Q6GZX4|001R_FRG3G Putative transcription factor 001R OS=Frog virus 3 (isolate Goorha) GN=FV3-001R PE=4 SV=1
	MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPS
	EKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLD
	AKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHL
	EKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDD
	SFRKIYTDLGWKFTPL
	
	Example output:
	>Q6GZX4 sp|Q6GZX4|001R_FRG3G Putative transcription factor 001R OS=Frog virus 3 (isolate Goorha) GN=FV3-001R PE=4 SV=1
	MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPS
	EKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLD
	AKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHL
	EKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDD
	SFRKIYTDLGWKFTPL
	'''
	uniprot_dir = file_directory
	fasta_files = [input_file_name]

	os.chdir(uniprot_dir)
	#open output file
	output_file = output_file_name
	f = open(output_file, 'w')
	

	## read individual fasta files and reformat header
	for i in range(len(fasta_files)):
		with open(fasta_files[i], 'rb') as fastafile:
			for line in fastafile:
				if line.startswith(">"):
					new_header = parse_uniprot_header(line)
					f.write(new_header)
				else:
					f.write(line)

	f.close()
	
### Index the formated Uniprot Fasta file

def index_uniprot_fasta(index_file_name,input_file,format_input):
	'''
	Function uses BioPython to index the Uniprot fasta file and 
	#sorted(uniprot_02122016)[:10]
	
	Argument:
	index_file_name -- selected nae for index fasta file; eg "HUMAN_March_2013_protgraphic_format.idx"
	input_file -- name of input sequence file; Eg 'HUMAN_March_2013_protgraphic_format.fasta' (fasta is required)
	format_input -- format of input sequence file (fasta is required); eg 'fasta'
	
	## Test function 
	print uniprot_HUMAN_March_2013['K7EIV4'].description
	print uniprot_HUMAN_March_2013['K7EIV4'].seq
	
	'''
	## Index sequence file with Biopython
	index_seq_file = SeqIO.index_db(index_file_name,input_file,format_input)
	
	return index_seq_file
	
## Function to split multiple accesion numbers

def split_accession(accession_num):
	"""
	The functions splits accession numbers if multiple are grouped
	
	Argument:
	Input: string of accession numbers list; eg 'P02533;P08779'
	Output: First accesssion number from the list; eg 'P02533'
	
	##Test function
	test_string = 'P02533;P08779'
	print type(test_string)
	print split_accession(test_string)
	"""
	id_list = accession_num.split(';')
	accession_num_format = id_list[0]
	
	return accession_num_format



def parse_thermo_psms(index_dir, uniprot_index_file, thermo_file_csv):
	'''
	The function reads in a thermo_psms_peptide file and parses indivdual line/peptides to 
	caluculate the start and stop postion of the peptide compared to the full length protein 
	
	When multiple accession numbers are detected the first one is selected using 
	split_accession function.
	
	Individual peptide sequences are compared to full length protein sequences using 
	the indexed_fasta database. The start and stop position of the peptide are computed 
	by re.match function. If the acccesion does not match the index database keys, 
	'0' is assigned to start and stop position.
	
	Argument: 
	index_dir -- Directory of indexed fasta file
	uniprot_index_file -- File name of indexed_fasta file
	thermo_file_csv -- Input thermo_psms_peptide file as .csv format
	
	Input:
	
	
	Output:	
		
	'''
	#accesstion_num = final_dataframe['Protein Group Accessions']
	#seq_peptide = final_dataframe['Sequence']
	## iniiatlize indexed fasta Uniprot file
	uniprot_dir = index_dir
	os.chdir(uniprot_dir)
	uniprot_HUMAN_March_2013 = SeqIO.index_db(uniprot_index_file)
	
	## input one sample thermo file
	# Initialize an empty Pandas dataframe.
	final_dataframe = pd.DataFrame()
	# Read in the thermo_psms_peptide files as .csv format
	final_dataframe = pd.read_csv(thermo_file_csv)
	
	
	
	pep_start_list = [None] * len(final_dataframe.index)
	pep_end_list = [None] * len(final_dataframe.index)
	accesstion_num_list = [None] * len(final_dataframe.index)
	
	#uniprot_keys = uniprot_HUMAN_March_2013.
	
	for index,row in final_dataframe.iterrows():
		# Create a field for peptide sequence and protein accession number
		seq_peptide = final_dataframe.loc[index,'Sequence'].upper()
		accesstion_num = final_dataframe.loc[index,'Protein Group Accessions']
    
    
    ## Skip the search if the accesstion number is neumeric
    if isinstance(accesstion_num, (int, long, float)):
        pep_start_list[index] = 0
        pep_end_list[index] = 0
        accesstion_num_list[index] = accesstion_num
		
   
    ## Split accesstion_num in case of multiple: split_accession(accession_num)
    if ";" in accesstion_num:
		accesstion_num = split_accession(accesstion_num)
		accesstion_num_list[index] = accesstion_num
    
    
    # Find the start and stop position of the peptide string compared to 
    if not accesstion_num in uniprot_HUMAN_March_2013:
        pep_start_list[index] = 0
        pep_end_list[index] = 0
	else:
		#if accesstion_num in uniprot_HUMAN_March_2013.keys:
		seq_protein = str(uniprot_HUMAN_March_2013[accesstion_num].seq)
		n = re.search(seq_peptide, seq_protein)
		if n:
			pep_start_list[index] = n.start() + 1
			pep_end_list[index] = n.end()
            
	final_dataframe['accesstion_num'] = accesstion_num_list
	final_dataframe['pep_start'] = pep_start_list
	final_dataframe['pep_end'] = pep_end_list
	
	return final_dataframe