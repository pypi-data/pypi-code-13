# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 15:34:04 2016

@author: astha

    Copyright (C) 2016   Inria

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Description: This module is an implementation of the algorithm presented in 
             P. Alquier and B. Guedj (2016), "A Sharp Oracle Inequality for 
             Bayesian Non-Negative Matrix Factorization" (arXiv preprint).

Requirement: Script has been tested on 
             "PACBayesianNMF"   v0.1.0
             "numpy"            v1.11.0
             "matplotlib"       v1.5.0
             "cv2"              v2.4.11

Purpose:    This script is written to load data for digits as given by 
            train.txt. Each row is a digit represented by label as first
            column followed by flattened 16x16 image represented as a array
            of 256 elements.
            
            Each element is preprocessed to belong to a number between [0,1]
            Then the conditions for block gradient descent are set and algorithm
            is applied to generate U, V, crit and out as output.
            U  and V   :are factors of the original dataMatrix.
            crit       :is an array of distance of estimated matrix
                        UV from original dataMatrix 
            out        :list of values of exit condition of the three loops.
                        This can be used for debugging purposes 

    See script in bin for sample usage of the package 
"""
from pacbayesiannmf import *
import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt
################## Loading Data into a matrix #################################
# List of the images in database 
dataList = []
labels = []
print "*********** Loading data **************"
# change the os.walk location to where database if located 
for root, dirs,files in os.walk("database"):
    for name in files: 
        temp = os.path.join(root,name)
        # so that if there are other files, they don't give an error 
        # can use it to filter out some data points 
        if '_' in temp: 
            im = cv2.imread(temp,cv2.IMREAD_GRAYSCALE)
            # reshape(-1): Return a contiguous flattened array
            vector = im.reshape(-1)
            dataList.append(vector)
            labels.append(name.split('_')[0])
            print name
print"************ Data loaded ****************"
print"Convert data into a 2D matrix"
print"With values in range(0,1)"
# create a matrix out of the List of vectors            
dataMatrix = np.matrix(dataList)
# data matrix contains only 0s and 1s 
dataMatrix= dataMatrix.astype(float)/255
#shape of dataMatrix 
shp =  dataMatrix.shape
if len(shp) != 2:
    print "Error: Please change the script for image to have a 2d matrix"
    print "       Current Shape of Matrix is:"+str(shp)
elif np.min(dataMatrix) < 0 or np.max(dataMatrix) > 1:
    print "Error: Values not between 0 and 1"
    print "       Please modify script to adjust values"
else:
    print"*******Call to blockGradientDescent******"
    z = blockGradientDescent(dataMatrix,2)
    z.setConditionOnAllSteps(1e-4,1e-6,1e-6)
    (U,V,crit,out)= z.applyBlockGradientDescent(printflag = 1)
    print"*******End of blockGradientDescent*******"
    ########################## Plot #######################################
    V = V*255
    #U = U*255
    V[V < 0] = 0
    V[V > 255] = 255
    #U[U < 0] = 0
    #U[U > 255] = 255
    V.astype(int)
    
    f, axarr = plt.subplots(2,3)
    axarr[0,0].imshow(np.reshape(V[:,0],(16,16)),cmap='Greys_r')
    axarr[0,1].imshow(np.reshape(V[:,1],(16,16)),cmap='Greys_r')
    axarr[1,2].plot(crit)
    ############################# END #########################################
#################### End of the script ########################################