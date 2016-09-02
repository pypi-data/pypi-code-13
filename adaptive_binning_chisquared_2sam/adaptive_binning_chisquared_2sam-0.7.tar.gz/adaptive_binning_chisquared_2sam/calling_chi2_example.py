#!/usr/bin/python
from chi2_regular_binning import *
from chi2_adaptive_binning import *
from chi2_plots import *
import os

def example_call():
	orig_name="gaussian_same_projection_redefined__0_1__0_75"
	title="Gauss 0.1 0.75"
	dim_list = [1,2,3]
	systematics_fraction = 0.01

	comp_file_list_list = []
	adaptive_binning=False
	for dim_data in dim_list:
		comp_file_list=[]
		for i in range(1):
			comp_file_list.append((os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_10000_0.0_1.0_1.0_{0}.txt".format(i,dim_data),os.environ['MLToolsDir']+"/Dalitz/gaussian_samples/gaussian_same_projection_on_each_axis/gauss_data/gaussian_same_projection_on_each_axis_redefined_{1}D_10000_0.0_1.0_0.75_{0}.txt".format(i,dim_data)))
		comp_file_list_list.append(comp_file_list)
	if adaptive_binning==True:
		number_of_splits_list = [1,2]
		#chi2_adaptive_binning.chi2_adaptive_binning(orig_name, dim_list, comp_file_list_list,number_of_splits_list)
		chi2_adaptive_binning_wrapper(title,orig_name, dim_list, comp_file_list_list,number_of_splits_list,systematics_fraction)
	else:
		single_no_bins_list=[2,3,5]
		chi2_regular_binning_wrapper(title,orig_name, dim_list, comp_file_list_list,single_no_bins_list,systematics_fraction)	

if __name__ == "__main__":
	example_call()
