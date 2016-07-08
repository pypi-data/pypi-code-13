#Hailey Haut

#PTM Parser

import pandas as pd
import os
import glob
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from collections import Counter
import csv
import re
#import math

def read_peptide(directory,file_pattern,analysis_type):
	"""
	A function that will go through a file of IPAS peptide files and will organize the results in 
	a Pandas dataframe.
	
	Arguments: directory, a string of the location where the file containing the peptide documents are.
	Return: df, a Pandas dataframe.
	"""
	print(directory,file_pattern)
	## Change to directory with files
	os.chdir(directory)
	# Initialize an empty dictionary to be added to the empty Pandas dataframe later.
	final_dataframe = pd.DataFrame()
	
	# Make sure the folder is not empty. 
	# If the folder is empty, create an empty dataframe with column headers
	# and return the empty dataframe. 
	if os.listdir(directory) == [] or os.listdir(directory) == ['.DS_Store']:
		return "Empty directory!"
	
	# Create an identifier for each chunk of files based on the file name and add to dataframe.
	for document in glob.glob(file_pattern):
		df = pd.read_csv(document,encoding="cp1252") ##py35
		filename_list = [document]*len(df.index)
		df['File Name'] = filename_list
		
		# PEAKS Parsing
		if "peaks" in analysis_type:
			df.columns = df.columns.str.replace("Protein Accession", "protein.Accession")
			df.columns = df.columns.str.replace("Peptide", "peptide.seq")
			df.columns = df.columns.str.replace("Start", "peptide.seqStart")
			df = peaks_parser(df)
		
		#Thermo Parsing
		elif "thermo" in analysis_type:
			df.columns = df.columns.str.replace("accesstion_num", "protein.Accession")
			df.columns = df.columns.str.replace("pep_start", "peptide.seqStart")
			#df.columns = df.columns.str.replace("Modifications", "peptide.modification")
			#df.columns = df.columns.str.replace("Spectrum File", "File Name")
			df.columns = df.columns.str.replace("Sequence", "peptide.seq")
			df = thermo_parser(df)
		
		# Waters Strict Filtration
		elif "waters_strict" in analysis_type:
			df.to_csv("original_df.csv")
			df = strict_parse(df)
			df.to_csv("FILTER.csv")
		
		# Waters no filtration
		else:
			df = df
		
		df = df[["File Name","protein.Accession", "peptide.modification", "peptide.seq", "peptide.seqStart", "peptide.seqLength"]]

		# Call helper function, peptide_parser(document) to add columns and information to the large dataframe.
		df = peptide_parser(df)
		
		if df.empty:
			print("DataFrame is empty!")
		
		# Add this new dataframe to the existing aggregate dataframe and update it.
		result = pd.concat([final_dataframe, df], axis = 0)
		## re-index concat dataframe to remove duplicate indices **********
		final_dataframe = result.reset_index(drop=True)
	
	final_dataframe.to_csv('Data_here.csv')
	return final_dataframe

def thermo_parser(dataframe):
	"""
	A helper function for read_peptide(directory). This function parses out the pertinent columns from the 
	thermo csv document and will return the results in a dataframe.

	Modification format: C22(Propionamide); M8(Oxidation) --> Propionamide+C(22);Propionamide+C(34)
	
	Argument: dataframe, a Pandas dataframe created from the experiment csv.
	Return: dataframe, the changed Pandas dataframe that is compatible with the rest of the code. 
	"""
	length_list = []
	mods_of_mods = []
	
	dataframe = nan_dropper_thermo(dataframe)
	
	for index,row in dataframe.iterrows():
		# Create a field to determine the peptide length
		start = dataframe.loc[index,"peptide.seqStart"]
		end = dataframe.loc[index,"pep_end"]
		length_list.append(float(end)-float(start)+1)
		
		# Determine if there is a valid modification
		temp_pattern = dataframe.loc[index,"Modifications"]
		temp_mod_str = ""
		while isinstance(temp_pattern,str) and len(str(temp_pattern)) > 0:
			# Check if the element is the first in a series of modifications
			if re.search(r"([a-zA-Z])(\d+)\(([a-zA-z]+)\)\;\s", temp_pattern):
				m = re.search(r"([a-zA-Z])(\d+)\(([a-zA-z]+)\)\;\s", temp_pattern)
				
			# Check if the element is the only modification or the last one in a series.
			elif re.search(r"([a-zA-Z])(\d+)\(([a-zA-z]+)\)", temp_pattern):
				m = re.search(r"([a-zA-Z])(\d+)\(([a-zA-z]+)\)", temp_pattern)
			temp_mod = m.group(3) + "+" + m.group(1) + "(" + m.group(2) + ")"
	
			# Add the result to a cumulative string
			if temp_mod_str == "":
				temp_mod_str = temp_mod
			else:
				temp_mod_str = temp_mod_str + ";" + temp_mod
			span_m = m.span()
			temp_pattern = temp_pattern[span_m[1]:]
		
		mods_of_mods.append(temp_mod_str)
		
	dataframe["peptide.modification"] = mods_of_mods
	dataframe["peptide.seqLength"] = length_list
		
	#dataframe.to_csv('Thermo Results.csv')
	return dataframe
	
def nan_dropper_thermo(df):
	"""
	This function uses columns from the original dataframe that meet certain parameters in order
	to determine if the sample meets the criteria. 
	"""
	df = df.dropna(subset=["pep_end"])
	df = df.dropna(subset=["peptide.seqStart"])
	df = df.dropna(subset=["protein.Accession"])
	return df
	
def strict_parse(df):
	"""
	This function uses columns from the original dataframe that meet certain parameters in order
	to determine if the sample meets the criteria. 
	"""
	return df[(df["peptide.MatchedProducts"] >= 5) & (df["peptide.AutoCurate"] == "Green") & (df["precursor.deltaMhpPPM"].abs() <= float(5))]
	
def peaks_parser(dataframe):
	"""
	A helper function for read_peptide(directory). This function parses out the pertinent columns from the 
	peaks csv document and will return the results in a dataframe.
	
	Arguments: dataframe, a Pandas Dataframe created from the experiment csv.
	Return: Larger dataframe
	
	peptide.modification
	"""
	# The mass weights and modifications associated with those weights. 
	modifications = {"6.02": "SILAC", "71.04":"Propionamide", "15.99":"Methionine oxidation", "79.97":"Phosphorylation", "14.0266":"Mono-Methylation", "28.0532":"Di-Methylation", "42.0797":"Tri-Methylation", "42.0367":"Acetylation", "100.0728":"Succinylation" }
	
	# If the input is "No file," set defaults for an empty dictionary.
	if dataframe.empty:
		return "Dataframe is empty!"
	
	# Create some container lists.
	length_list = []
	mods_of_mods = []
	pep_list_total = []
		
	for index,row in dataframe.iterrows():
		# Create a field to determine the peptide length
		start = dataframe.loc[index,"peptide.seqStart"]
		end = dataframe.loc[index,"End"]
		length_list.append(float(end)-float(start)+float(1))
		mod_name_list = []
		
		# Parse substitutions
		temp_pattern = dataframe.loc[index,"peptide.seq"]
		while "sub" in temp_pattern:
			m = re.search(r"(\w)\(sub\s(\w)\)", temp_pattern)
			while "+" in temp_pattern:
				n = re.search(r"(\(\+\d+\.\d+\))", temp_pattern)
				start_end = n.span()
				temp_pattern = temp_pattern[:start_end[0]]+temp_pattern[start_end[1]:]
			sub_num = temp_pattern.index('(sub')-2
			mod_name_list.append(m.group(2)+"-"+"Substitution+"+m.group(1)+"("+str(sub_num)+")")
			temp_pattern = temp_pattern[:sub_num+2]+temp_pattern[sub_num+9:]
								
		# Parse weights on the plus sign. 
		if "+" in dataframe.loc[index,"peptide.seq"]:
			mod_list = []
			stripped_string = dataframe.loc[index,"peptide.seq"]
			t_pat = dataframe.loc[index,"peptide.seq"]
	
			# Indices start at "1" after the first dot. 
			while "+" in t_pat:
				while "sub" in t_pat:
					n = re.search(r"(\(\w+\s\w\))", t_pat)
					start_end = n.span()
					t_pat = t_pat[:start_end[0]]+t_pat[start_end[1]:]
				partitioned_string = t_pat.partition("+")
				second_part = partitioned_string[2].partition(")")
				mod_list.append(second_part[0])
				mod_letter = partitioned_string[0][-2]
				mod_number = stripped_string.index("(") - 2
				stripped_string = t_pat.partition("(")[0]+t_pat.partition(")")[2]
				if second_part[0] in modifications.keys():
					mod_name_list.append(modifications[second_part[0]]+"+"+mod_letter+"("+str(mod_number)+")")
				t_pat = stripped_string
				
		# If there are no modifications, do the following: 	
		else:
			mod_list = ["None"]
			if len(mod_name_list) == 0:
				mod_name_list.append("None")
			#mod_name_list = ["None"]
			
		# Combine small lists. 
		mods_of_mods.append(', '.join(mod_list))
		pep_list_total.append(';'.join(mod_name_list))
		
	# Add these lists to the PEAKS dataframe.
	dataframe["peptide.seqLength"] = length_list
	dataframe["pep.mod numbers"] = mods_of_mods
	dataframe["peptide.modification"] = pep_list_total
	
	dataframe.to_csv("PEAKS Parsed.csv")
	return dataframe
	
def peptide_parser(dataframe):
	"""
	A helper function for read_peptide(directory). This function parses out the pertinent columns from the 
	csv document and will return the results in a new dataframe.
	
	Arguments: dataframe, a Pandas Dataframe created from the experiment csv.
	Return: Larger dataframe
	"""
	
	# If the input is "No file," set defaults for an empty dictionary.
	if dataframe.empty:
		return "Dataframe is empty!"
	
	# Create list containers that will be lists of lists.
	end_list = []
	mods_of_mods = []
	big_num_list = []
	big_original = []
	big_specific = []
	big_mod_pos = []
	#big_mp_lset = []
	big_type = []
	big_combo = []
	
	for index,row in dataframe.iterrows():
		# Create a field where the peptide stops (end position)
		start = dataframe.loc[index,"peptide.seqStart"]
		length = dataframe.loc[index,"peptide.seqLength"]
		end_list.append(float(start)+float(length))
			
		# Separate the modifications by semi-colon and collect in a list.
		if ";" in dataframe.loc[index,"peptide.modification"]:
			mod_list = []
			mod_string = dataframe.loc[index,"peptide.modification"]
			while ";" in mod_string:
				partitioned_string = mod_string.partition(";")
				mod_list.append(partitioned_string[0])
				mod_string = partitioned_string[2]
				if ";" not in mod_string:
					mod_list.append(mod_string)
		else:
			mod_list = [dataframe.loc[index,"peptide.modification"]]
		mods_of_mods.append(', '.join(mod_list))

		# Make list to hold all modifications
		num_list = []
		original_mod_list = []
		specific_mod_list = []
		mod_type = []
		
		# Partition each modification by type and position
		for mod in mod_list:
			partitioned_mod = mod.partition('+')
			mod_type.append(partitioned_mod[0])
			if partitioned_mod[2] == "":
				aa_mod = partitioned_mod[0].partition('(')
			else:
				aa_mod = partitioned_mod[2].partition('(')
			aa_num = aa_mod[2].partition(')')
			amino_num = aa_num[0]
			
			if amino_num.isdigit():
				amino_num = int(amino_num)
			
			# Account for case when there are no modifications
			if amino_num != "":
				num_list.append(amino_num)
			else:
				num_list.append("None")
			
			if "Glyco" in mod:
				original_mod_list.append("N")
			else:
				original_mod_list.append(aa_mod[0])
			
			# Account for multiple potential modifications and pick the one that matches. 
			if len(aa_mod[0]) > 1:
				if "Glyco" in mod: 
					specific_mod_list.append("N")
				elif isinstance(amino_num, int) or isinstance(amino_num, float): 
					sp_mod = int(amino_num)
					seq_spot = dataframe.loc[index,"peptide.seq"]
					specific_mod_list.append(seq_spot[int(sp_mod-1)])
				else: 
					specific_mod_list.append(aa_mod[0])
			else:
				specific_mod_list.append(aa_mod[0])
				
		# Modification Position + Start (Position on Protein where mod takes place)
		# Make list of all modification positions, get unique positions, return num unique positions.
		mod_position_in_list = []
		combo_list = []
		#unique_pos_set = set([])
		for num_idx in range(len(num_list)):
			if isinstance(num_list[num_idx], int) or isinstance(num_list[num_idx], float):
				mod_pos = dataframe.loc[index,"peptide.seqStart"]
				mod_position_in_list.append(int(num_list[num_idx])+int(mod_pos))
				#unique_pos_set.add(int(num_list[num_idx])+int(mod_pos))
			else:
				end = int(start)+int(length)
				mod_position_in_list.append(str(start)+"-"+str(end))
				#unique_pos_set.add("None")
		
		for mod_idx in range(len(specific_mod_list)):
			combo_list.append(specific_mod_list[mod_idx]+str(mod_position_in_list[mod_idx]))
				
		# Add all information to large list containers
		big_num_list.append(str(num_list)[1:-1])
		big_combo.append(combo_list)
		big_original.append(', '.join(original_mod_list))
		big_specific.append(', '.join(specific_mod_list))
		big_mod_pos.append(mod_position_in_list)
		#big_mp_lset.append(str(list(unique_pos_set))[1:-1])
		big_type.append(mod_type)
		
	dataframe["End Position"] = end_list
	dataframe["pep.mod LIST"] = mods_of_mods
	dataframe["Num PTM Type"] = big_num_list
	dataframe["Modification Position"] = big_mod_pos
	#dataframe["Unique Mod Position"] = big_mp_lset
	dataframe["Original Mod List"] = big_original
	dataframe["Specific Mod List"] = big_specific
	dataframe["Mod Type"] = big_type
	dataframe["Combo List"] = big_combo
	return dataframe
	
def filter_by_mod(dataframe, *args):
	"""
	A function that filters the dataframe based on the modification that is searched for. 
	
	Possible types:
	Oxidation, None, Propionamide, Monomethyl, dimethyl
	"""
	# Make a list of the arguments
	arg_set = set([])
	for key in args:
		arg_set.add(key)
	
	# Initialize a new dataframe for the filtered results
	small_df = pd.DataFrame()
	
	# Create a list of sets for all modifications
	mod_list = dataframe["Mod Type"].tolist()
	m_pos = dataframe["Modification Position"].tolist()
	n_ptm = dataframe["Num PTM Type"].tolist()
	o_mod = dataframe["Original Mod List"].tolist()
	s_mod = dataframe["Specific Mod List"].tolist()
	pm_list = dataframe["pep.mod LIST"].tolist()
	p_mod = dataframe["peptide.modification"].tolist()
	c_mod = dataframe["Combo List"].tolist()
	
	mod_lset = []
	spot_list = []
	m_copy = []
	for mod_l in mod_list:
		temp_set = set([])
		temp_list = []
		t_copy = []
		for imod in range(len(mod_l)):
			temp_set.add(mod_l[imod])
			t_copy.append(mod_l[imod])
			if mod_l[imod] not in arg_set:
				temp_list.append(imod)
			else:
				temp_list.append("SKIP")
		spot_list.append(temp_list)
		mod_lset.append(temp_set)
		m_copy.append(t_copy)
	
	#print(spot_list[:25],"\t",n_ptm[:25])
	#print parse_by_index(spot_list[:25],n_ptm[:25])
	#return
	
	dataframe["Mod Type"] = parse_by_index(spot_list,m_copy)
	dataframe["Modification Position"] = parse_by_index(spot_list,m_pos)
	dataframe["Num PTM Type"] = parse_by_index(spot_list,n_ptm)
	dataframe["Original Mod List"] = parse_by_index(spot_list,o_mod)
	dataframe["Specific Mod List"] = parse_by_index(spot_list,s_mod)
	dataframe["pep.mod LIST"] = parse_by_index(spot_list,pm_list)
	dataframe["peptide.modification"] = parse_by_index(spot_list,p_mod)
	dataframe["Combo List"] = parse_by_index(spot_list,c_mod)
	
	# Iterate over the rows of the dataframe
	for index,row in dataframe.iterrows():

		# Check if the parameters given are in the modifications. If so, add this to the dataframe.
		if bool(arg_set.intersection(mod_lset[index])):
			temp_df = dataframe.iloc[index]
			result = pd.concat([small_df, temp_df], axis = 1)
			small_df = result
			
		# Add section to account for where the modification is in the row
		# Ex. Oxidation is second, therefore parse row so only oxidation info is left
		# If there are multiple of the same modification, keep info bc same mod.
		
	small_df = small_df.transpose()
	small_df.to_csv('Data.csv')
	return small_df

def parse_by_index(idx_list, data_list):
	"""
	A helper function for the filter function that parses out multiple modifications.
	
	Arguments: idx_list, a list of lists of indices that do not match the modification and 
				data_list, a list of lists of a field that correspond to the indices.
	Return: final_list, a list of lists of parsed data accoording to the indices given. 
	"""
	# Initialize a final list to be returned later
	final_list = []
	
	# Iterate through each list of lists
	for i_lst in range(len(data_list)):	
		if isinstance(idx_list[i_lst],str):
			continue
		# Iterate through each sublist's contents. 
		for idx_position in range(len(idx_list[i_lst])-1,-1,-1):
			
			# Depending on the position, change the sublist.
			if idx_position == idx_list[i_lst][idx_position]:
				if isinstance(data_list[i_lst], list):
					data_list[i_lst].pop(idx_position)
				else:
					if ";" in data_list[i_lst]:
						split_data = [x.strip() for x in data_list[i_lst].split(';')]
						split_data.pop(idx_position)
						data_list[i_lst] = split_data
					elif "," in data_list[i_lst]:
						split_data = [x.strip() for x in data_list[i_lst].split(',')]
						split_data.pop(idx_position)
						data_list[i_lst] = split_data
			else:
				continue
		
		# Add the sublist to the final list.
		final_list.append(data_list[i_lst])
	
	return final_list
	
def unique_PTM(df):
	"""
	A function that uses a dataframe to identify the unique modification locations for each protein
	accession and modification.
	
	Arguments: df, a Pandas dataframe from either read_peptide() or filter_by_mod()
			   modification, a string that is the desired modification that is being analyzed.
	Return: final_df, a new Pandas dataframe that contains the protein accession, all locations for 
	a given modification, unique locations, and the number of unique locations.
	"""
	# Create lists from columns in original dataframe
	protein_acc = df["protein.Accession"].tolist()
	mod_pos = df["Combo List"].tolist()
	mod_letter = df["Specific Mod List"].tolist()

	# Initialize dictionary containers for positions
	all_mods_dict = {}
	lset = {}
	unique_count = {}
	mod_let_dict = {}
	
	# Create lists of all positions
	for idx in range(len(protein_acc)):
		mod_let_dict[protein_acc[idx]] = mod_letter[idx]
		if protein_acc[idx] not in all_mods_dict.keys():
			all_mods_dict[protein_acc[idx]] = mod_pos[idx]
		else:
			all_mods_dict[protein_acc[idx]] = all_mods_dict[protein_acc[idx]] + mod_pos[idx]
		
	# With those lists, get the unique positions by turning them into sets. Get how many elements are in the sets.
	for key in all_mods_dict.keys():
		all_pos = all_mods_dict[key]
		temp_set = set(all_pos)
		unique_count[key] = len(temp_set)
		lset[key] = temp_set
		
	#non_unique_df = pd.DataFrame([non_unique_dict])
	#non_unique_df = non_unique_df.transpose()
	#non_unique_df.to_csv('test.csv')
	
	# Create the dataframe and format it
	final_df = pd.DataFrame([all_mods_dict,mod_let_dict, lset, unique_count])
	final_df = final_df.transpose()
	final_df.columns = ["All Positions/Letters","Modification Letter","Unique Positions","Number of Unique Positions"]
	final_df.to_csv('A_Unique_DF.csv')
	
	return final_df

def unique_PTM_count(df_uniquePTM):
	"""
	Function to count the non-unique modification positions by 
	protein ID and position
	
	Arguments: df_uniquePTM, a Pandas dataframe from unique_PTM()
	This dataframe has protein IDs and all the modifiations associated with them.
	Return: non_unique_df, a new Pandas dataframe that contains the protein accession and postions
	along with the counts of PTM for that position.	
	"""
	non_unique_dict = {}
	for index,row in df_uniquePTM.iterrows():
		# Read each line of the PTM filtered dataframe 
		all_position = df_uniquePTM.loc[index,"All Positions/Letters"]
		# count the occurance of redundant PTM sites
		occurences = Counter(all_position)
		# Parse all the unique position and protein IDs using a loop and put into
		# new dictionary
		for i in range(len(occurences.keys())):
			# Create a new key and values for the data dictionary
			new_index = index+"|"+str(list(occurences.keys())[i])  ##py35
			new_value = str(list(occurences.values())[i])          ##py35
			non_unique_dict[new_index] = new_value
			#if "None" in new_index:
			#	print new_index, new_value, occurences.values()[i]
				
			#df_postionPTM_count.loc[new_index] = new_value
		
	# Make a dataframe from the proteinID postion counts data dictionary
	non_unique_df = pd.DataFrame.from_dict(non_unique_dict, orient='index')
	return non_unique_df	
	
	
def venn_comparison(non_unique_df, col1, col2):
	"""
	A function that will graphically represent the common/uncommon non-unique locations
	for all experiments.
	
	Argument: non_unique_df, a Pandas Dataframe generated from unique_PTM_count.
	Return: Nothing, but different matplotlib graphs will shwo up on the screen and can be stored.
	"""
	## make a list of all the indexes for the pandas dataframe
	indices = non_unique_df.index
	## make a list of selected columns from the pandas dataframe
	loc_mark1 = non_unique_df[col1].tolist()
	loc_mark2 = non_unique_df[col2].tolist()
	
	loc_set1 = set([])
	loc_set2 = set([])
	
	## make a set of non-zero indices
	for idx in range(len(indices)):
		if str(loc_mark1[idx]) != 'nan':
			loc_set1.add(indices[idx])
		if str(loc_mark2[idx]) != 'nan':
			loc_set2.add(indices[idx])
	
	## Plot the venn diagram
	v = venn2([loc_set1, loc_set2], (str(col1), str(col2)))
	plt.title("MisClevages")
	plt.show()
	
	
#output_file = "Test_monomethy.txt"
#f = open(output_file, 'w')	

def generate_report():
	"""
	The 'main' function for the PTM Parser. Calling this function will start executing the different functions
	in the proper order and it will return a PDF report.
	"""
	
	#directory = r'O:\Hanash_Lab_GPFS\Amin\LabDataProcessing\HaileyProjects\PythonProteomicsPipeline\Data\IPAS0801_Nuclear_monoMethyl_MCle_2'
	directory = r'C:\HaileyProjects\IPAS933'
	#file_pattern = 'IPAS0801_Nuclear_SG39to40_IA_final_peptide.csv'
	#file_pattern = 'IPAS933_Surface_SG01to22_IA_final_peptide.csv'
	#file_pattern = 'MCF7_sur_protein-peptides.csv'
	#file_pattern = 'Thermo_Test.csv'
	file_pattern = 'IPAS_0323MultiConsensus_psms_v2.csv'
	print("file pattern below")
	#file_pattern = 'IPAS0801_Nuclear_SG43to44_IA_final_peptide.csv'
	os.chdir(directory)
	dataframe = read_peptide(directory, file_pattern)
	df = filter_by_mod(dataframe, "Methyl")
	df_unique = unique_PTM(df)
	non_unique = unique_PTM_count(df_unique)
	#non_unique.to_csv('Not Unique.csv')


def generate_report_input(directory, file_pattern, modification,analysis_type):
	"""
	The 'main' function for the PTM Parser. Calling this function will start executing the different functions
	in the proper order and it will return a PDF report.
	
	Arguments: directory_input, file_pattern_input, modification
	
	"""	
	print(directory,file_pattern,modification)
	os.chdir(directory)
	dataframe = read_peptide(directory,file_pattern,analysis_type)
	df = filter_by_mod(dataframe,modification)
	df_unique = unique_PTM(df)
	
	return unique_PTM_count(df_unique)
	
	print("complete search\n")