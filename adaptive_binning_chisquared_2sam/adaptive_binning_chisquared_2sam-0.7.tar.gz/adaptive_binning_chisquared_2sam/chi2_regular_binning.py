import sys 
import chi2_plots
import itertools

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
#single_no_bins_list_list= ast.literal_eval(sys.argv[2])
#dim_list = ast.literal_eval(sys.argv[3])
#comp_file_list_list = ast.literal_eval(sys.argv[4])

def chi2_regular_binning_wrapper(orig_title, orig_name, dim_list, comp_file_list_list,single_no_bins_list,systematics_fraction):

	sample1_name="original"
	sample2_name="modified"

	DEBUG = True


	##############################################################################
	for dim_index, dim_data in enumerate(dim_list):
		print("We are now in "+str(dim_data) + " Dimensions")
		#comp_file_list=[]
		comp_file_list = comp_file_list_list[dim_index]
		#for i in range(100):

			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/higher_dimensional_gauss/gauss_data/data_high" +str(dim_data)+"Dgauss_10000_0.5_0.1_0.0_{0}.txt".format(i),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/higher_dimensional_gauss/gauss_data/data_high"+str(dim_data)+"Dgauss_10000_0.5_0.1_0.01_{0}.txt".format(i))) 
			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/legendre/legendre_data/data_legendre_contrib0__1__10__sample_{0}.txt".format(i),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/legendre/legendre_data/data_legendre_contrib0__1__9__sample_{0}.txt".format(i)))
			#comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_1000_0.6_0.2_0.1_{0}.txt".format(i,dim_data),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_1000_0.6_0.2_0.075_{0}.txt".format(i,dim_data)))
		#print(comp_file_list)

		for single_no_bins in single_no_bins_list:
			score_list=[]
			counter = 0
			for comp_file_0,comp_file_1 in comp_file_list:
				name = orig_name + "_" +str(dim_data) + "D_chi2_" + str(single_no_bins)+ "_bins"
				title= orig_title +" " +str(dim_data) + "D "      + str(single_no_bins)+ " bins"
				print("single_no_bins : ",single_no_bins)
				print("Operating of files :"+comp_file_0+"   "+comp_file_1)

				#extracts data from the files
				features_0=np.loadtxt(comp_file_0,dtype='d')
				features_1=np.loadtxt(comp_file_1,dtype='d')

				result = chi2_regular_binning(features_0,features_1,single_no_bins,systematics_fraction,title,name,not counter,DEBUG)	
				score_list.append(result)
				counter+=1


                        with open(name+"_p_values", "wb") as test_statistics_file:
                                for score in score_list:
                                        test_statistics_file.write(str(score)+"\n")


			#if dim_data==2: os.rename(str(dim_data) + "D_" + str(single_no_bins)+"_bins" +"_bin_definitions_2D.png",name+"_bin_definitions_2D.png")
                        #if dim_data==1: os.rename(str(dim_data) + "D_" + str(single_no_bins)+"_bins" +"_bin_definitions_1D.png",name+"_bin_definitions_1D.png")
                        chi2_plots.histo_plot_pvalue(score_list,50,"p value","Frequency",title,name)


def chi2_regular_binning(features_0,features_1,single_no_bins,systematics_fraction=0.0,title= "title", name="name", PLOT = True, DEBUG = False):
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
		no_bins = [single_no_bins]*no_dim       

		np.random.shuffle(data)

		labels=data[:,-1]

		X_values= data[:,:-1]
		X_max   = np.amax(data,axis=0)[:-1] 
		X_min   = np.amin(data,axis=0)[:-1]
		X_total_width = (np.subtract(X_max,X_min))
		X_width = (np.divide(np.subtract(X_max,X_min),no_bins))
		del data

		#Scaling        
		X_values = X_values - X_min[None,:]
		X_values = X_values / X_total_width[None,:]

		#b = X_values[:,0]
		#print("b[b[:]>2].shape[0] : \n", b[b[:]>2].shape[0] )  
		data = np.concatenate((X_values, labels[:,None]), axis=1)

		bin_points_dict = {}

		key_list = [list(p) for p in itertools.product(range(single_no_bins), repeat=no_dim)]
		#for c in combinations_with_replacement(range(single_no_bins), no_dim):
		for c in key_list:
			bin_points_dict[','.join(map(str,c))]= [0,0]

		print("bin_points_dict : \n",bin_points_dict)

		for i in range(no_0+no_1):
			#bin position
			#x_bin=int(np.floor((Xx_values[i]-Xx_min)/Xx_width))
			#y_bin=int(np.floor((Xy_values[i]-Xy_min)/Xy_width))

			pos_bins=np.floor(X_values[i,:]*no_bins).astype(int)
			pos_bins[pos_bins[:]==single_no_bins]=single_no_bins-1
			#print(pos_bins)

			if(labels[i]==0): 
				bin_points_dict[','.join(map(str,pos_bins))][0]+=1
			if(labels[i]==1):
				bin_points_dict[','.join(map(str,pos_bins))][1]+=1

		print("bin_points_dict : \n",bin_points_dict)
		

		Scp2 =  []
		signed_Scp2 = []
		keys = []

		for bin_key, bin_entry in bin_points_dict.items():
			bin_sample0 = bin_entry[0]
			bin_sample1 = bin_entry[1]
			if(systematics_fraction*float(bin_sample0)!=0.): bin_sample0 += int(round(np.random.normal(0.,systematics_fraction*float(bin_sample0))))
			if(systematics_fraction*float(bin_sample1)!=0.): bin_sample1 += int(round(np.random.normal(0.,systematics_fraction*float(bin_sample1))))
			bin_points_dict[bin_key] = [bin_sample0, bin_sample1]				

			keys.append(bin_key)
			Scp2.append(np.square(float(bin_sample1-bin_sample0))/(float(bin_sample1)+float(bin_sample0)+np.square(float(bin_sample1)*systematics_fraction)+np.square(float(bin_sample1)*systematics_fraction)))
			signed_Scp2.append(np.square(float(bin_sample1-bin_sample0))/(float(bin_sample1)+float(bin_sample0)+np.square(float(bin_sample1)*systematics_fraction)+np.square(float(bin_sample1)*systematics_fraction))*np.sign(bin_sample1-bin_sample0))

		keys,Scp2,signed_Scp2 = zip(*sorted(zip(keys,Scp2,signed_Scp2)))



		#nansum ignores all the contributions that are Not A Number (NAN)
		Chi2 = np.nansum(Scp2)
		if DEBUG:
			print("Chi2")
			print(Chi2)
		dof=no_bins[0]
		for dim in range(1,no_dim):
			dof *= no_bins[1]
		dof-=1
	
		pvalue= 1 - stats.chi2.cdf(Chi2,dof)

		if DEBUG:
			print("Chi2/dof : {0}".format(str(Chi2/dof)))

			print("pvalue : {0}".format(str(pvalue)))

		if PLOT:
				if no_dim==1: chi2_plots.regular_binning_1Dplot(data,single_no_bins,title,name)
				if no_dim==2: chi2_plots.regular_binning_2Dplot(keys, signed_Scp2,single_no_bins,X_values,title,name)

		return pvalue







