import numpy as np
import matplotlib
from matplotlib.pylab import *
import matplotlib.pyplot as plt
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
        ax1_pred_0.set_title(atitle)
        plt.xlim([0,1])

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax1_pred_0.text(0.85, 0.95, textstr, transform=ax1_pred_0.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

        fig_pred_0.savefig(aname+"_p_values_plot.png")
        #plt.close(fig_pred_0)

def adaptive_binning_plot(bin_boundaries_dict,signed_Scp2_dict,number_of_splits,X_values,name):
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
		fig.savefig(name+"_bin_definitions.png")
		print("The plot {}_bin_definitions.png has been made".format(name))
	else:
		print("You can only make this plot in 2D")



