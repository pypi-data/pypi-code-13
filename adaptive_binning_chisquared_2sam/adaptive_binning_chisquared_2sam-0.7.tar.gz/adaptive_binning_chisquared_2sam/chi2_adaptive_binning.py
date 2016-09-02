from __future__ import print_function
import sys 
import chi2_plots 
import random
import ast
"""
This script can be used to get the p value for the Miranda method (=chi squared). It takes input files with column vectors corresponding to 
features and lables. 
"""

print(__doc__)
import sys
#sys.path.insert(0,'../..')
import os
from scipy import stats
import numpy as np
#import matplotlib.pyplot as plt 
#import numpy.matlib
#from matplotlib.colors import Normalize

#from sklearn.preprocessing import StandardScaler

##############################################################################
# Setting parameters
#
#orig_name= sys.argv[1]
#number_of_splits_list= ast.literal_eval(sys.argv[2])
#print("number_of_splits_list : ", number_of_splits_list)
#dim_list = ast.literal_eval(sys.argv[3])
#comp_file_list_list = ast.literal_eval(sys.argv[4])


def chi2_adaptive_binning_wrapper(orig_title, orig_name, dim_list, comp_file_list_list,number_of_splits_list,systematics_fraction):

	sample1_name="original"
	sample2_name="modified"

	DEBUG = False


	##############################################################################
	for dim_index, dim_data in enumerate(dim_list):
		print("We are now in "+str(dim_data) + " Dimensions")
		#comp_file_list=[]
		comp_file_list = comp_file_list_list[dim_index]
		#for i in range(2):

			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/higher_dimensional_gauss/gauss_data/data_high" +str(dim_data)+"Dgauss_10000_0.5_0.1_0.0_{0}.txt".format(i),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/higher_dimensional_gauss/gauss_data/data_high"+str(dim_data)+"Dgauss_10000_0.5_0.1_0.01_{0}.txt".format(i))) 
			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/legendre/legendre_data/data_legendre_contrib0__1__10__sample_{0}.txt".format(i),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/legendre/legendre_data/data_legendre_contrib0__1__9__sample_{0}.txt".format(i)))
			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_1000_0.6_0.2_0.1_{0}.txt".format(i,dim_data),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_1000_0.6_0.2_0.075_{0}.txt".format(i,dim_data)))
		#print(comp_file_list)

		score_dict = {}
		for number_of_splits in number_of_splits_list:
			score_dict[str(number_of_splits)]=[]
		
		counter = 0
		for comp_file_0,comp_file_1 in comp_file_list:
			print("Operating of files :"+comp_file_0+"   "+comp_file_1)

			#extracts data from the files
			features_0=np.loadtxt(comp_file_0,dtype='d')
			features_1=np.loadtxt(comp_file_1,dtype='d')

			#only make a plot for the first data set
			results_list=chi2_adaptive_binning(features_0,features_1,number_of_splits_list,systematics_fraction,orig_title,orig_name, not counter,DEBUG)
			for number_of_splits_index, number_of_splits in enumerate(number_of_splits_list):
				score_dict[str(number_of_splits)].append(results_list[number_of_splits_index])	

			counter+=1

                for number_of_splits in number_of_splits_list:
                        name = orig_name + "_" +str(dim_data) + "D_chi2_" + str(number_of_splits) + "_splits"
                        title= orig_title+ " " +str(dim_data) + "D "      + str(number_of_splits) + " splits" 
			print("score_dict[{}] : ".format(number_of_splits), score_dict[str(number_of_splits)])
                        with open(name+"_adaptive_binning_p_values", "wb") as test_statistics_file:
                                for score in score_dict[str(number_of_splits)]:
                                        test_statistics_file.write(str(score)+"\n")
			#if dim_data==2: os.rename("name_"+str(dim_data) + "D_" + str(number_of_splits) + "_splits"+"_bin_definitions_2D.png",name+"_bin_definitions_2D.png")
                        #if dim_data==1: os.rename("name_"+str(dim_data) + "D_" + str(number_of_splits) + "_splits"+"_bin_definitions_1D.png",name+"_binning_bin_definitions_1D.png")
                        chi2_plots.histo_plot_pvalue(score_dict[str(number_of_splits)],50,"p value","Frequency",title,name)





def chi2_adaptive_binning(features_0,features_1,number_of_splits_list,systematics_fraction=0.0,title = "title", name="name", PLOT = True, DEBUG = False):
	"""This function takes in two 2D arrays with all features being columns"""

	max_number_of_splits = np.max(number_of_splits_list)
	#determine how many data points are in each sample
	no_0=features_0.shape[0]
	no_1=features_1.shape[0]

	#Give all samples in file 0 the label 0 and in file 1 the feature 1
	label_0=np.zeros((no_0,1))
	label_1=np.ones((no_1,1))

	#Create an array containing samples and features.
	data_0=np.c_[features_0,label_0]
	data_1=np.c_[features_1,label_1]

	data=np.r_[data_0,data_1]

	no_dim = data.shape[1]-1

	np.random.shuffle(data)

	#print("data.shape : ", data.shape)
	labels=data[:,-1]

	X_values= data[:,:-1]
	X_max   = np.amax(data,axis=0)[:-1] 
	X_min   = np.amin(data,axis=0)[:-1]
	X_total_width = (np.subtract(X_max,X_min))
	del data

	#Scaling	
	X_values = X_values - X_min[None,:]
	X_values = X_values / X_total_width[None,:]

	#b = X_values[:,0]
	#print("b[b[:]>2].shape[0] : \n", b[b[:]>2].shape[0] )	
	data = np.concatenate((X_values, labels[:,None]), axis=1)

	#print("X_values.shape : ",X_values.shape)
	starting_boundary = []
	for i in range(no_dim):
		starting_boundary.append([0.0,1.0])
	#Each key has the following stricture: # of splits and for each split if it was closer (a) or further away from (b) the origin. The original bin is "0"
	#For example "2ab" means it is the bin that was closer to the origin for the first split and further away for the second one.
	bin_boundaries_dict = {'0' : np.array(starting_boundary)}
	bin_points_dict = {'0' : data}

	for split_number in range(1,1+max_number_of_splits):
		for bin_key, bin_boundary in bin_boundaries_dict.items():
			if str(split_number-1) in bin_key:
				variances= np.var(bin_points_dict[bin_key][:,:-1], axis=0)
				#print("\nvariances : ", variances)
				dim_to_be_sliced = np.argmax(variances)
				#print("dim_to_be_sliced : ",dim_to_be_sliced)
				#print("bin_points_dict[bin_key] : ",bin_points_dict[bin_key])
				#print("bin_points_dict[bin_key][:,dim_to_be_sliced] : ",bin_points_dict[bin_key][:,dim_to_be_sliced])
				median = np.median(bin_points_dict[bin_key][:,dim_to_be_sliced])
				#print("median : ",median)

				a_bin_boundary, b_bin_boundary = bin_boundary.copy(), bin_boundary.copy()
				#print("a_bin_boundary : ",a_bin_boundary)
				a_bin_boundary[dim_to_be_sliced,1] = median
				b_bin_boundary[dim_to_be_sliced,0] = median
				bin_boundaries_dict[str(split_number)+bin_key[1:]+'a'] = a_bin_boundary
				bin_boundaries_dict[str(split_number)+bin_key[1:]+'b'] = b_bin_boundary
				
				a_points, b_points = [],[] 
				for event_number in range(bin_points_dict[bin_key].shape[0]):
					if bin_points_dict[bin_key][event_number,dim_to_be_sliced] < median: a_points.append(bin_points_dict[bin_key][event_number,:].tolist())
					else: b_points.append(bin_points_dict[bin_key][event_number,:].tolist())
				
				bin_points_dict[str(split_number)+bin_key[1:]+'a'] = np.array(a_points)
				bin_points_dict[str(split_number)+bin_key[1:]+'b'] = np.array(b_points)
				#If a bin contains no particles it should be deleted
				if len(a_points)==0: 
					del bin_points_dict[str(split_number)+bin_key[1:]+'a']
					del bin_boundaries_dict[str(split_number)+bin_key[1:]+'a']
				if len(b_points)==0: 
					del bin_points_dict[str(split_number)+bin_key[1:]+'b']
					del bin_boundaries_dict[str(split_number)+bin_key[1:]+'b']

		
	bins_sample01_dict= {}
	signed_Scp2_dict= {}
	results_list = []

	for number_of_splits in number_of_splits_list:
		print("\nnumber_of_splits : ",number_of_splits,"\nsystematics_fraction : ",systematics_fraction)
		bins_sample0, bins_sample1 = [] , [] 
		for bin_key, bin_points in bin_points_dict.items():
			if str(number_of_splits) in bin_key:
				labels_in_bin = bin_points[:,-1]
				#print("labels_in_bin : ",labels_in_bin)
				bin_sample0 = np.count_nonzero( labels_in_bin == 0)
				bin_sample1 = np.count_nonzero( labels_in_bin == 1)
				#print("bin_sample0 : ",bin_sample0) 
				#print("bin_sample1 : ",bin_sample1) 
				#simulate uncertainties 
				if(systematics_fraction*float(bin_sample0)!=0.): bin_sample0 += int(round(np.random.normal(0.,systematics_fraction*float(bin_sample0))))
				if(systematics_fraction*float(bin_sample1)!=0.): bin_sample1 += int(round(np.random.normal(0.,systematics_fraction*float(bin_sample1))))
				bins_sample01_dict[bin_key]=[bin_sample0,bin_sample1]
				signed_Scp2_dict[bin_key] = np.square(float(bin_sample1-bin_sample0))/(float(bin_sample1)+float(bin_sample0)+np.square(float(bin_sample1)*systematics_fraction)+np.square(float(bin_sample1)*systematics_fraction))*np.sign(bin_sample1-bin_sample0)
				#print("\n\nbin_sample0 : ",bin_sample0, "\n bins_sample0 : ", bins_sample0 )
				#print("type(bin_sample0) : ",type(bin_sample0), "  type(bins_sample0) : ",type(bins_sample0))
				bins_sample0.append(bin_sample0)
				#print("  bins_sample0 : ", bins_sample0, "\n\n" )
				bins_sample1.append(bin_sample1)
		bins_sample0, bins_sample1 = np.array(bins_sample0,dtype=float), np.array(bins_sample1, dtype=float)
		print("bins_sample0 : ",bins_sample0,"\n bins_sample1 : ",bins_sample1)
		#element wise subtraction and division
		Scp2 = ((bins_sample1-bins_sample0)**2)/ (bins_sample1+bins_sample0+(systematics_fraction*bins_sample1)**2+(systematics_fraction*bins_sample0)**2 )
		#Scp2 =  np.divide(np.square(np.subtract(bins_sample1,bins_sample0)),np.add(bins_sample1,bins_sample0))
		if DEBUG:
			print(Scp2)

		#nansum ignores all the contributions that are Not A Number (NAN)
		Chi2 = np.nansum(Scp2)
		if DEBUG:
			print("Chi2")
			print(Chi2)
		dof=bins_sample0.shape[0]-1
	
		pvalue= 1 - stats.chi2.cdf(Chi2,dof)
		
		print("\nThe p value for Scp2 = ",Scp2," and Chi2 = ", Chi2, " is ",pvalue,"\n\n")
		if DEBUG:
			print(bins_sample0)
			print(bins_sample1)
			print("Chi2/dof : {0}".format(str(Chi2/dof)))

			print("pvalue : {0}".format(str(pvalue)))

		results_list.append(pvalue)

		if PLOT: 
			if no_dim==1: chi2_plots.adaptive_binning_1Dplot(bin_boundaries_dict,data,number_of_splits,title+" "+str(no_dim) + "D "+str(number_of_splits)+ " splits ",name+"_"+str(no_dim) + "D_chi2_"+str(number_of_splits)+"_splits")
			if no_dim==2: chi2_plots.adaptive_binning_2Dplot(bin_boundaries_dict,signed_Scp2_dict,number_of_splits,X_values,title+" "+str(no_dim) + "D"+str(number_of_splits)+ " splits ",name+"_"+str(no_dim) + "D_chi2_"+str(number_of_splits)+"_splits")

	return results_list 






