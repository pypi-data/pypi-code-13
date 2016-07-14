'''
Created on Jul 2, 2016

@author: tavis
'''
import tilescraper as ts
import beijingpollutioncompiler as pc
import image2lmdb as i2l
import numpy as np
import datetime
import math
from PIL import Image
import os , inspect


pollution_dict = {}
this_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))


def getPollutionDictionary():
    """Fetches the dictionary of pollution indices (by SQL date) into a global variable"""
    global pollution_dict
    if not pollution_dict:
        pollution_dict = pc.fetchDailyAverage()
    return pollution_dict


def loadVisualTrainingDataToArray():
    """Loads the visual training data from the resources directory into an array of (SQL date,image),
    swaps the axes, and gets rid of invalid observations
    """
    pollution_dictionary = getPollutionDictionary()
    visual_training_array = ts.loadStreamToIndexedArray("2012-06-24","2015-07-02",
                                                        prefix=project_dir+"/resources/visual-images/visual-",
                                                        extension=".jpg")
    visual_training_image_array = []
    visual_training_outcome_array = []
    for this_element in visual_training_array:
        today = this_element[0]
        this_date_pollution = pollution_dictionary.get(today)
        today_object = datetime.date(int(today[0:4]),int(today[5:7]),int(today[8:10]))
        tomorrow_object = today_object + datetime.timedelta(days=1)
        tomorrow = str(tomorrow_object.year) + "-" + \
            ("0" if tomorrow_object.month < 10 else "") + str(tomorrow_object.month) + \
            "-" + ("0" if tomorrow_object.day < 10 else "") + str(tomorrow_object.day)
        next_date_pollution = pollution_dictionary.get(tomorrow)
        this_date_image_array = np.array(this_element[1]).swapaxes(1,2).swapaxes(0,1)
        if this_date_pollution is not None and this_date_pollution > 0 and \
                next_date_pollution is not None and next_date_pollution > 0 and \
                np.sum(this_date_image_array) > int(128*128*4):
            visual_training_image_array.append(this_date_image_array)
            visual_training_outcome_array.append(math.log(next_date_pollution/this_date_pollution))
    return ( visual_training_image_array , visual_training_outcome_array)


def loadVisualTestDataToArray():
    """Loads the visual test data from the resources directory into an array of (SQL date,image),
    swaps the axes, and gets rid of invalid observations
    """
    pollution_dictionary = getPollutionDictionary()
    visual_test_array = ts.loadStreamToIndexedArray("2015-07-03","2016-07-02",
                                                        prefix=project_dir+"/resources/visual-images/visual-",
                                                        extension=".jpg")
    visual_test_image_array = []
    visual_test_outcome_array = []
    for this_element in visual_test_array:
        today = this_element[0]
        this_date_pollution = pollution_dictionary.get(today)
        today_object = datetime.date(int(today[0:4]),int(today[5:7]),int(today[8:10]))
        tomorrow_object = today_object + datetime.timedelta(days=1)
        tomorrow = str(tomorrow_object.year) + "-" + \
            ("0" if tomorrow_object.month < 10 else "") + str(tomorrow_object.month) + \
            "-" + ("0" if tomorrow_object.day < 10 else "") + str(tomorrow_object.day)
        next_date_pollution = pollution_dictionary.get(tomorrow)
        this_date_image_array = np.array(this_element[1]).swapaxes(1,2).swapaxes(0,1)
        if this_date_pollution is not None and this_date_pollution > 0 and \
                next_date_pollution is not None and next_date_pollution > 0 and \
                np.sum(this_date_image_array) > int(128*128*4):
            visual_test_image_array.append(this_date_image_array)
            visual_test_outcome_array.append(math.log(next_date_pollution/this_date_pollution))
    return ( visual_test_image_array , visual_test_outcome_array)

def loadAerosolTrainingDataToArray():
    """Loads the aerosol training data from the resources directory into an array of (SQL date,image),
    swaps the axes, and gets rid of invalid observations
    """
    pollution_dictionary = getPollutionDictionary()
    aerosol_training_array = ts.loadStreamToIndexedArray("2012-06-24","2015-07-02",
                                                        prefix=project_dir+"/resources/aerosol-images/aerosol-", 
                                                        extension=".jpg")
    aerosol_training_image_array = []
    aerosol_training_outcome_array = []
    for this_element in aerosol_training_array:
        today = this_element[0]
        this_date_pollution = pollution_dictionary.get(today)
        today_object = datetime.date(int(today[0:4]),int(today[5:7]),int(today[8:10]))
        tomorrow_object = today_object + datetime.timedelta(days=1)
        tomorrow = str(tomorrow_object.year) + "-" + \
            ("0" if tomorrow_object.month < 10 else "") + str(tomorrow_object.month) + \
            "-" + ("0" if tomorrow_object.day < 10 else "") + str(tomorrow_object.day)
        next_date_pollution = pollution_dictionary.get(tomorrow)
        this_date_image_array = np.array(this_element[1]).swapaxes(1,2).swapaxes(0,1)
        if this_date_pollution is not None and this_date_pollution > 0 and \
                next_date_pollution is not None and next_date_pollution > 0 and \
                np.sum(this_date_image_array) > int(128*128*4):
            aerosol_training_image_array.append(this_date_image_array)
            aerosol_training_outcome_array.append(math.log(next_date_pollution/this_date_pollution))
    return ( aerosol_training_image_array , aerosol_training_outcome_array)

def loadAerosolTestDataToArray():
    """Loads the aerosol test data from the resources directory into an array of (SQL date,image),
    swaps the axes, and gets rid of invalid observations
    """
    pollution_dictionary = getPollutionDictionary()
    aerosol_test_array = ts.loadStreamToIndexedArray("2015-07-03","2016-07-02",
                                                        prefix=project_dir+"/resources/aerosol-images/aerosol-",                                                        extension=".jpg")
    aerosol_test_image_array = []
    aerosol_test_outcome_array = []
    for this_element in aerosol_test_array:
        today = this_element[0]
        this_date_pollution = pollution_dictionary.get(today)
        today_object = datetime.date(int(today[0:4]),int(today[5:7]),int(today[8:10]))
        tomorrow_object = today_object + datetime.timedelta(days=1)
        tomorrow = str(tomorrow_object.year) + "-" + \
            ("0" if tomorrow_object.month < 10 else "") + str(tomorrow_object.month) + \
            "-" + ("0" if tomorrow_object.day < 10 else "") + str(tomorrow_object.day)
        next_date_pollution = pollution_dictionary.get(tomorrow)
        this_date_image_array = np.array(this_element[1]).swapaxes(1,2).swapaxes(0,1)
        if this_date_pollution is not None and this_date_pollution > 0 and \
                next_date_pollution is not None and next_date_pollution > 0 and \
                np.sum(this_date_image_array) > int(128*128*4):
            aerosol_test_image_array.append(this_date_image_array)
            aerosol_test_outcome_array.append(math.log(next_date_pollution/this_date_pollution))
            print("Appending " + str(math.log(next_date_pollution/this_date_pollution)) + " and image to test aerosol array.")
    return ( aerosol_test_image_array , aerosol_test_outcome_array)


def calculateMeanImage(image_array,save_as=""):
    """Returns an image whose pixels are equal to the mean of each pixel in the image array and optionally saves it
    
    Arguments:
    image_array -- an array of images, each an RGB image of shape 3x128x128
    save_as     -- the file to save to.  Nothing will be saved if it is blank or omitted
    """
    image_running_sum = np.zeros((3,128,128))
    image_count = 0
    for this_image in image_array:
        for i in range(0,3):
            image_running_sum[i] = image_running_sum[i] + this_image[i]
        image_count += 1
    for i in range (0,3):
        image_running_sum[i] = image_running_sum[i]*(1/float(image_count))    
    if save_as != "":
        avg_image_array = np.uint8(np.rint(image_running_sum),casting='unsafe')
        avg_image = Image.fromarray(avg_image_array.swapaxes(0,1).swapaxes(1,2))
        avg_image.save(save_as)
    
    return avg_image_array

if __name__ == '__main__':

    (visual_training_image_array , visual_training_outcome_array ) = loadVisualTrainingDataToArray()
    
    visual_training_image_average = calculateMeanImage(visual_training_image_array,project_dir+"resources/mean_files/training_visual_mean.jpg")
    for this_image in visual_training_image_array:
        this_image -= visual_training_image_average

    i2l.data2LMDB(visual_training_image_array, visual_training_outcome_array, project_dir+"/resources/training_visual_array_lmdb")

    (aerosol_training_image_array , aerosol_training_outcome_array ) = loadAerosolTrainingDataToArray()

    aerosol_training_image_average = calculateMeanImage(aerosol_training_image_array,project_dir+"/resources/mean_files/training_aerosol_mean.jpg")
    for this_image in aerosol_training_image_array:
        this_image -= aerosol_training_image_average

    i2l.data2LMDB(aerosol_training_image_array, aerosol_training_outcome_array, project_dir+"/resources/training_aerosol_array_lmdb.png")

    (visual_test_image_array , visual_test_outcome_array ) = loadVisualTestDataToArray()

    visual_test_image_average = calculateMeanImage(visual_test_image_array,project_dir+"/resources/mean_files/test_visual_mean.jpg")
    for this_image in visual_test_image_array:
        this_image -= visual_test_image_average

    i2l.data2LMDB(visual_test_image_array, visual_test_outcome_array, project_dir+"/resources/test_visual_array_lmdb")

    (aerosol_test_image_array , aerosol_test_outcome_array ) = loadAerosolTestDataToArray()

    aerosol_test_image_average = calculateMeanImage(aerosol_test_image_array,project_dir+"/resources/mean_files/test_aerosol_mean.jpg")
    for this_image in aerosol_test_image_array:
        this_image -= aerosol_test_image_average

    i2l.data2LMDB(aerosol_test_image_array, aerosol_test_outcome_array, project_dir+"/resources/test_aerosol_array_lmdb")


    

    #aerosol_mosaic_stream = ts.TileScraper(2000,5,32,5,32)
    #aerosol_mosaic_stream.pullMosaicStream("2012-04-24","2015-07-02", "MODIS_Terra_Aerosol", project_dir+"resources/aerosol-images/image-")


    #dict = ts.getFormat()
    #print(dict)

#AQI token: e0b6686ae09afac0ce24a2d900792379b9871fcb
#https://worldview.earthdata.nasa.gov/?p=geographic&l=VIIRS_SNPP_CorrectedReflectance_TrueColor(hidden),MODIS_Aqua_CorrectedReflectance_TrueColor(hidden),MODIS_Terra_CorrectedReflectance_TrueColor(hidden),AIRS_Prata_SO2_Index_Day(hidden),AIRS_CO_Total_Column_Day,MODIS_Terra_Aerosol(hidden),Reference_Labels(hidden),Reference_Features,Coastlines&t=2016-04-17&v=112.0    7788935367951,26.740860067407684,125.44605341617951,35.03773506740768

