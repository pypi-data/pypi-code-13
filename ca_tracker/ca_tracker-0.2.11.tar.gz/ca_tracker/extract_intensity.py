import pandas as pd 
import pickle
import helper as h
import numpy as np
import os

import logging
from logging.config import fileConfig


#fileConfig('ca_tracker/config/logging_config.ini')
logger = logging.getLogger(os.path.basename(__file__))

def measureIntPerFramePerLabel(exp_filename, labelvol, times, max_frames,\
         imagefolder, channel_dict={'ca' : 1, 'sp' : 1}):
    
    logger.info('start measure meanint')
    dict_mint = {}
    dict_frames = {}

    labels_all = np.unique(labelvol.flatten())[1:]

    


    #init dict
    for label in labels_all:
        dict_mint[label] = []
        dict_frames[label] = []


    
    for i in range(max_frames):
        progress = round(i/float(max_frames) * 100., 1)
        
        labelvol_index = times.frames_to_sp[i]
        label_mat = labelvol[labelvol_index,:,:]
        labels = np.unique(label_mat.flatten())[1:]


        
        img_filename = times.filename[i]
        #select channel according the module type
        if h.is_ca_module_filename(img_filename):
            channel = channel_dict['ca']
        else:
             channel = channel_dict['sp']

        path = imagefolder + exp_filename + \
            '_singlechannel/' + img_filename + '_c00' + str(channel) + '.tif'
        
        logger.info('measure ca intensity of %s: %s percent done',\
            os.path.basename(path), str(progress))
        im = h.loadImage(path)
        
        

        for label in labels:
            mean_int = measureMeanIntPerLabel(im, label_mat, label)
            
            dict_mint[label].append(mean_int)
            dict_frames[label].append(i)
    return dict_mint, dict_frames       


def measureMeanIntPerLabel(im, label_mat, label):
    pixels = im[label_mat==label]
    if len(pixels) == 0:
        mean_int = np.nan
    else:
        mean_int = np.mean(pixels)
    return mean_int    





def extract_intensity_for_channel(channel_dict, times, labelvol, classes, exp_filename, imagefolder, resultsfolder):
    #measure intensity frame by frame
    max_frames = times['filename'].count()
    d_mint, d_frames = measureIntPerFramePerLabel(exp_filename, labelvol\
        , times, max_frames, imagefolder, channel_dict=channel_dict)


    #convert dict data tp data tables
    dat = pd.DataFrame(index=times.index)
    for label in d_mint.keys():
        dat[label] = pd.Series(d_mint[label], index=d_frames[label])

    classes_stable = classes[classes.is_stable]
    labels_speck = classes_stable[classes_stable.is_specking]['label'].tolist()
    labels_hom = classes_stable[~classes_stable.is_specking]['label'].tolist()


    #divide into specking and non specking cells
    dat_speck = dat[labels_speck] #intensity data per frame for specking cells
    dat_hom = dat[labels_hom] #intensity data per frame for homogeneous cells

    #export data
    channel_suffix = h.format_channel_suffix(channel_dict) 
    dat_speck.to_csv(resultsfolder + exp_filename + '_intensities_speck_' + channel_suffix + '.csv')
    dat_hom.to_csv(resultsfolder + exp_filename + '_intensities_hom_' + channel_suffix + '.csv')







def extract_intensity(exp_filename, config):

    resultsfolder = config['data_locations']['resultsfolder']
    imagefolder = config['data_locations']['imagefolder']

    logger.info('map measurment channels from config file')
    channels_ca = config['channel_mapping']['readout_channels_ca']
    channels_sp = config['channel_mapping']['readout_channels_sp']
    channel_dicts = h.format_readout_channels(channels_ca, channels_sp)

    logger.info('nr of readout channels: %s', str(len(channel_dicts)))


    


    #data import
    times = pd.read_csv(resultsfolder + exp_filename + '_timetable.csv')
    classes = pd.read_csv(resultsfolder + exp_filename + '_classes.csv')
    imdat = pickle.load(open(resultsfolder + exp_filename + '_trackdata.pickle', 'rb'))
    labelvol = imdat['track_labelvol'].astype(int)

    counter = 1
    for channel_dict in channel_dicts:
        logger.info('readout channel %s maps to following image channels: %s'\
            , counter, channel_dict)
        counter +=1
        extract_intensity_for_channel(channel_dict, times, labelvol, classes\
            , exp_filename, imagefolder, resultsfolder)

    
















