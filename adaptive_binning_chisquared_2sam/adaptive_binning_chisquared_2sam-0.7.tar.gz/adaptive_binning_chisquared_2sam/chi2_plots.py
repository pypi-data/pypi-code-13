import numpy as np
#import matplotlib
#from matplotlib.pylab import *
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import time


def histo_plot_pvalue(U_0,abins,axlabel,aylabel,atitle,aname):
        bins_probability=np.histogram(U_0,bins=abins)[1]

        #Finding the p values corresponding to 1,2 and 3 sigma significance.
        no_one_std_dev=sum(i < (1-0.6827) for i in U_0)
        no_two_std_dev=sum(i < (1-0.9545) for i in U_0)
        no_three_std_dev=sum(i < (1-0.9973) for i in U_0)

        print(no_one_std_dev,no_two_std_dev,no_three_std_dev)

        with open(aname+"_p_values_1_2_3_std_dev.txt",'w') as p_value_1_2_3_std_dev_file:
                p_value_1_2_3_std_dev_file.write(str(no_one_std_dev)+'\t'+str(no_two_std_dev)+'\t'+str(no_three_std_dev)+'\n')

        #plt.rc('text', usetex=True)
        textstr = '$1\sigma=%i$\n$2\sigma=%i$\n$3\sigma=%i$'%(no_one_std_dev, no_two_std_dev, no_three_std_dev)


        # Making a histogram of the probability predictions of the algorithm. 
        fig_pred_0= plt.figure()
        ax1_pred_0= fig_pred_0.add_subplot(1, 1, 1)
        n0, bins0, patches0 = ax1_pred_0.hist(U_0, bins=bins_probability, facecolor='red', alpha=0.5)
        ax1_pred_0.set_xlabel(axlabel)
        ax1_pred_0.set_ylabel(aylabel)
        ax1_pred_0.set_title(atitle+ " p values")
        plt.xlim([0,1])

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax1_pred_0.text(0.85, 0.95, textstr, transform=ax1_pred_0.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

        fig_pred_0.savefig(aname+"_p_values_plot.png")
        #plt.close(fig_pred_0)

def adaptive_binning_2Dplot(bin_boundaries_dict,signed_Scp2_dict,number_of_splits,X_values,title,name):
	if X_values.shape[1]==2:
		fig= plt.figure()
		ax1= fig.add_subplot(1, 1, 1)	
		signed_Scp2_values = []
		for bin_key, bin_Scp2 in signed_Scp2_dict.items(): 
			if str(number_of_splits) in bin_key: 
				signed_Scp2_values.append(bin_Scp2)	
		norm = matplotlib.colors.Normalize(min(signed_Scp2_values),max(signed_Scp2_values))
		my_cmap = cm.get_cmap('Greys')
		
		ax1.scatter(X_values[:,0], X_values[:,1], c='black',s=5, lw = 0)

		for bin_key, bin_boundary in bin_boundaries_dict.items():
			if str(number_of_splits) in bin_key:
				#print("Boundaries : ",bin_boundary[0,0], bin_boundary[1,0], bin_boundary[0,1],bin_boundary[1,1])
				cd=ax1.add_patch(Rectangle((bin_boundary[0,0], bin_boundary[1,0]),bin_boundary[0,1]-bin_boundary[0,0] , bin_boundary[1,1]-bin_boundary[1,0],alpha=0.5, edgecolor="black",facecolor = my_cmap(norm(signed_Scp2_dict[bin_key])),linewidth=2))
	
		plt.xlim(0.0,1.0)
		plt.ylim(0.0,1.0)	
                plt.xlabel("normalised x feature")
                plt.ylabel("normalised y feature")
                plt.title(name + " bin definitions" )
		fig.savefig(name+"_bin_definitions_2D.png")
		print("The plot {}_bin_definitions_2D.png has been made".format(name))
	else:
		print("You can only make this plot in 2D")


def adaptive_binning_1Dplot(bin_boundaries_dict,data,number_of_splits,title,name):
	if data.shape[1]-1==1:
		data0    = data[data[:,-1]==0]
                data1    = data[data[:,-1]==1]
		#print("data0 : ",data0)
		features_0 = data0[:,:-1]
		features_1 = data1[:,:-1]
		#print("features_0 : ",features_0)

		fig= plt.figure()
		ax1= fig.add_subplot(1, 1, 1)
		#bin_sample01_list = []
		bin_boundaries = []
		bin_boundaries_lower = []
		for bin_key, bin_boundaries_in_dict in bin_boundaries_dict.items():
			if str(number_of_splits) in bin_key:
				#bin_sample01_list.append(bins_sample01)
				bin_boundaries.append(bin_boundaries_in_dict[0][1])
				bin_boundaries_lower.append(bin_boundaries_in_dict[0][0])

		bin_boundaries = sorted(bin_boundaries)
                #bin_boundaries, features = zip(*sorted(zip(bin_boundaries,bin_sample01_list)))
		#print("bin_boundaries : ",bin_boundaries)
		bin_boundaries = [min(bin_boundaries_lower)] + list(bin_boundaries)
		#print("bin_boundaries : ",bin_boundaries)

		#print("bin_sample01_list : ",np.array(bin_sample01_list))

		#bin_sample0 = np.array(bin_sample01_list)[:,0]
                #bin_sample1 = np.array(bin_sample01_list)[:,1]
		#print("features_0.shape : ",features_0.shape,"\nfeatures_1.shape : ",features_1.shape)
		plt.hist(features_0,bins=bin_boundaries,color='red',label='original',alpha=0.4,normed=True)
		plt.hist(features_1,bins=bin_boundaries,color='blue',label= 'modified',alpha=0.4,normed=True)
                
		plt.xlabel("normalised feature")
                plt.title(title + " bin definitions" )
		fig.savefig(name+"_bin_definitions_1D.png")
                print("The plot {}_bin_definitions_1D.png has been made".format(name))
        else:
                print("You can only make this plot in 1D")
		

def regular_binning_2Dplot(keys, signed_Scp2,single_no_bins,X_values,title,name):
        no_dim = X_values.shape[1]
	if no_dim==2:
		no_bins = [single_no_bins]*no_dim

                fig= plt.figure()
                ax1= fig.add_subplot(1, 1, 1)
                norm = matplotlib.colors.Normalize(np.min(signed_Scp2),np.max(signed_Scp2))
                my_cmap = cm.get_cmap('Greys')

                ax1.scatter(X_values[:,0], X_values[:,1], c='black',s=5, lw = 0)

		for key_index, key in enumerate(keys):
			key_list = np.array(key.split(',')).astype(int).tolist()
 

			bin_boundary = np.array([[float(key_list[0])/float(single_no_bins)  ,float(key_list[0]+1)/float(single_no_bins) ],[float(key_list[1])/float(single_no_bins)  ,float(key_list[1]+1)/float(single_no_bins)  ]])
			print("bin_boundary : ",bin_boundary)
			print("bin_boundary[0,0] : ",bin_boundary[0,0])
			print("signed_Scp2 : ", signed_Scp2)


			cd=ax1.add_patch(Rectangle((bin_boundary[0,0], bin_boundary[1,0]),bin_boundary[0,1]-bin_boundary[0,0] , bin_boundary[1,1]-bin_boundary[1,0],alpha=0.5, edgecolor="black",facecolor = my_cmap(norm(signed_Scp2[key_index])),linewidth=2))

                plt.xlim(0,1)
                plt.ylim(0,1)
                plt.xlabel("normalised x feature")
		plt.ylabel("normalised y feature")
                plt.title(title + " bin definitions" )

		fig.savefig(name+"_bin_definitions_2D.png")
                print("The plot {}_bin_definitions_2D.png has been made".format(name))
        else:
                print("You can only make this plot in 2D")

def regular_binning_1Dplot(data,single_no_bins,title,name):
        if data.shape[1]-1==1:
                data0    = data[data[:,-1]==0]
                data1    = data[data[:,-1]==1]
                #print("data0 : ",data0)
                features_0 = data0[:,:-1]
                features_1 = data1[:,:-1]

                fig= plt.figure()
                ax1= fig.add_subplot(1, 1, 1)

                plt.hist(features_0,bins=np.linspace(0,1,single_no_bins+1),color='red',label='original',alpha=0.4,normed=True)
                plt.hist(features_1,bins=np.linspace(0,1,single_no_bins+1),color='blue',label= 'modified',alpha=0.4,normed=True)
		plt.xlabel("normalised feature")
		plt.title(title + " bin definitions" )

                fig.savefig(name+"_bin_definitions_1D.png")
                print("The plot {}_bin_definitions_1D.png has been made".format(name))
        else:
                print("You can only make this plot in 1D")


























