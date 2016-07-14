'''
Created on Jul 13, 2016

@author: tavis
'''

import datetime
import tilescraper as ts
import numpy as np
import beijingpollutioncompiler as bpc
import sys
import caffe
from collections import defaultdict
from PIL import Image
import os , inspect
import math

"""
This program takes whatever model has been trained in the resources directory,
pulls the current Beijing AQI from the US embassy web site, pulls the MODIS
satellite data for the sample area for today, and predicts tomorrow's pollution.
It also produces a lot of very noisy output.....
"""


if __name__ == '__main__':

    this_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    
    visual_prototxt_file_path = os.path.join(project_dir,"resources/caffe_prototxt/beijing_pollution_test_visual_single_image.prototxt")
    visual_model_file_path = os.path.join(project_dir,"resources/caffe_models/beijing_pollution_model_visual.model")
    aerosol_prototxt_file_path = os.path.join(project_dir,"resources/caffe_prototxt/beijing_pollution_test_aerosol_single_image.prototxt")
    aerosol_model_file_path = os.path.join(project_dir,"resources/caffe_models/beijing_pollution_model_aerosol.model")
   
    today = datetime.date.today()

    today_visual_image = ts.pullMosaic("MODIS_Terra_CorrectedReflectance_TrueColor" , 41.0 , 114.0 , 37.0 , 118.0 , today.year , today.month , today.day, 128, 128)
    today_formatted_visual_image = np.array(today_visual_image).swapaxes(1,2).swapaxes(0,1)
    if np.sum(today_formatted_visual_image) > int(128*128*4):
        (current_aqi_string , measurement_time_string ) = bpc.getLatestReading() 
        current_aqi = float(current_aqi_string)
        image_mean = Image.open(os.path.join(project_dir,"resources/mean_files/training_visual_mean.jpg"))
        image_mean_array = np.array(image_mean).swapaxes(1,2).swapaxes(0,1)
        prediction_input = today_formatted_visual_image - image_mean_array 
        image_batch_array = np.zeros((1,3,128,128),dtype=np.float32)
        image_batch_array[0] = prediction_input.astype(np.float32)
        visual_net = caffe.Net(visual_prototxt_file_path, visual_model_file_path, caffe.TEST)
        visual_net.set_input_arrays(image_batch_array,np.zeros((1,1,1,1),dtype=np.float32))
        out = visual_net.forward()
        #The input outcomes were multiplied by 100 so we adjust here
        prediction = float(out['ip1'][0])/100
        print("Tomorrow's predicted pollution is " + current_aqi_string + "*exp(" + str(prediction) + ") = " + str(current_aqi*math.exp(prediction)) )
        
    else:
        print("Sorry, no visual satellite data from today yet.  Try again later.")


    today_aerosol_image = ts.pullMosaic("MODIS_Terra_Aerosol" , 41.0 , 114.0 , 37.0 , 118.0 , today.year , today.month , today.day, 128, 128)
    today_formatted_aerosol_image = np.array(today_aerosol_image).swapaxes(1,2).swapaxes(0,1)
    if np.sum(today_formatted_aerosol_image) > int(128*128*4):
        (current_aqi_string , measurement_time_string ) = bpc.getLatestReading() 
        current_aqi = float(current_aqi_string)
        image_mean = Image.open(os.path.join(project_dir,"resources/mean_files/training_aerosol_mean.jpg"))
        image_mean_array = np.array(image_mean).swapaxes(1,2).swapaxes(0,1)
        prediction_input = today_formatted_aerosol_image - image_mean_array 
        image_batch_array = np.zeros((1,3,128,128),dtype=np.float32)
        image_batch_array[0] = prediction_input.astype(np.float32)
        aerosol_net = caffe.Net(aerosol_prototxt_file_path, aerosol_model_file_path, caffe.TEST)
        aerosol_net.set_input_arrays(image_batch_array,np.zeros((1,1,1,1),dtype=np.float32))
        out = aerosol_net.forward()
        prediction = float(out['ip1'][0])/100
        print("Tomorrow's predicted pollution is " + current_aqi_string + "*exp(" + str(prediction) + ") = " + str(current_aqi*math.exp(prediction)) )
        
    else:
        print("Sorry, no aerosol satellite data from today yet.  Try again later.")
