import pandas as pd 
import trackpy as tp 

import logging
from logging.config import fileConfig
import os
#fileConfig('ca_tracker/config/logging_config.ini')
logger = logging.getLogger(os.path.basename(__file__))


def compute_trajectory_table(centroid_table, search_range, memory):

    t = tp.link_df(centroid_table, search_range, memory=memory)
    return t




def track_centroids(exp_filename, config):
    
    resultsfolder = config['data_locations']['resultsfolder']
    centroid_table = pd.read_csv(resultsfolder + exp_filename + '_centroid_table.csv')

    logger.info('compute trajectories for %s ...', exp_filename)
    trajectory_table = compute_trajectory_table(\
            centroid_table, config['tracking']['search_range'],\
            config['tracking']['memory'])

    trajectory_table.rename(columns=\
        {'x': 'y', 'y' : 'x', 'frame': 'Frame', 'particle': 'Trajectory'},\
        inplace=True)
    

    trajectory_table = trajectory_table[['x', 'y', 'Frame', 'Trajectory']]

    savename = exp_filename + '_trajectories.csv'
    logger.info('write trajectory data to %s', savename)

    trajectory_table.to_csv(resultsfolder + savename)