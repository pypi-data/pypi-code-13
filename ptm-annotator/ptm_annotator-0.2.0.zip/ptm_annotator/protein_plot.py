# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 16:06:28 2016

@author: AAMomin

Module that conatains functions to plot proteomics data
"""

# import ploting libraries
from matplotlib import pyplot as plt
from matplotlib_venn import venn2



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