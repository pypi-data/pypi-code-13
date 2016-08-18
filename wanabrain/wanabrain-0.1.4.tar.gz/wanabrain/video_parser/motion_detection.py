# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
from scipy.spatial.distance import euclidean
import math
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import warnings
warnings.filterwarnings('error')
import logging
import itertools

CHANGED_POINTS_FRACTION = 0.5
CHANGED_ORIENTATION_FRACTION = 0.6
CHANGE_THRESHOLD = 0.9
SEQ_THRESHOLD = 0.1

def cp_directions(new, old):
    """
    Compute the direction between two points

    Args:
        @type new: Tuple of int
        @param new: New keypoints

        @type new: Tuple of int
        @param new: Old keypoints

    Return:
        @type direction: float
        @param direction: Direction between the old and new points

        @type norm: float
        @param norm: Norm between the old and new points

        @type orientation: float
        @param orientation: Orientation between the old and new points
    """

    dist = [old[0] - new[0], old[1] - new[1]]
    norm = math.sqrt(dist[0] ** 2 + dist[1] ** 2)
    denom = new[0] - old[0]
    if denom == 0:
        denom = 0.000001
    orientation = math.degrees(math.atan((new[1] - old[1])/denom))
    if norm == 0:
        norm = 0.0001
    direction = [dist[0] / norm, dist[1] / norm]

    return direction, norm, orientation

def change_detection(norms):
    """
    Detect if the camera is fixed or moving

    Args:
        @type norms: Array-like of int
        @param norms: All norms from all the keypoints pairs

    Return:
        @type static: boolean
        @param static: True if the camera is fixed, False otherwise
    """

    norms = np.array(norms)
    changed_points = np.sum(norms > CHANGE_THRESHOLD)

    if changed_points > len(norms) * CHANGED_POINTS_FRACTION:
        static = False
    else:
        static = True

    return static

def orientation_detection(orientations, directions):
    """
    Detect in which direction the camera is moving

    Args:
        @type orientations: Array-like of float
        @param orientations: All orientation from all the keypoints pairs

        @type directions: Array-like of float
        @param directions: All directions from all the keypoints pairs

    Return:
        @type orientation: String
        @param orientation: The direction in which the camera is moving
    """

    str_orientations = []
    for orientation, direction in zip(orientations, directions):

        if (45 > orientation > -45) and direction[0] < 0:
            str_orientations.append('pano droite gauche')
        elif (45 > orientation > -45) and direction[0] > 0:
            str_orientations.append('pano gauche droite')
        elif (135 > orientation > 45) and direction[1] > 0:
            str_orientations.append('pano haut bas')
        elif (-45 > orientation > -135) and direction[1] > 0:
            str_orientations.append('pano haut bas')
        elif (135 > orientation > 45) and direction[1] < 0:
            str_orientations.append('pano bas haut')
        elif (-45 > orientation > -135) and direction[1] < 0:
            str_orientations.append('pano bas haut')

    all_orientations, counts = np.unique(str_orientations, return_counts=True)

    orientation = None
    for orient, count in zip(all_orientations, counts):
        if count > len(orientations) * CHANGED_ORIENTATION_FRACTION:
            orientation = orient

    return orientation

def zoom_detection(good_new, good_old, frame_width_center, frame_height_center):
    """
    Detect in which direction the camera is moving

    Args:
        @type good_new: Array-like of tuple of int
        @param good_new: All keypoints from the new frame

        @type good_old: Array-like of tuple of int
        @param good_old:  All keypoints from the preceding frame

        @type frame_width_center: float
        @param frame_width_center: coordinate of the width center

        @type frame_height_center: float
        @param frame_height_center: coordinate of the height center

    Return:
        @type zoom: String
        @param zoom: The zoom being done
    """

    zooms = []
    for old, new in zip(good_old, good_new):

        old_dist = math.fabs(math.sqrt( (old[0] - frame_width_center )**2 + (old[1] - frame_height_center)**2 ))
        new_dist = math.fabs(math.sqrt( (new[0] - frame_width_center )**2 + (new[1] - frame_height_center)**2 ))

        if new_dist < old_dist :
            zoom = 'zoom arriere'
        else:
            zoom = 'zoom avant'

        # print(zoom)

        zooms.append(zoom)

    all_zooms, counts = np.unique(zooms, return_counts=True)

    zoom = all_zooms[np.argsort(counts)[::-1][0]]

    return zoom

def motion_detection(cap):
    """
    Process the frames of a video to identify the motion of the camera

    Args:
        @type cap: VideoCapture object
        @param cap: A VideoCapture object corresponding to a video file encapsulated by OpenCV

    Return:
        @type movement: String
        @param movement: The motion of the camera
    """

    # params useful for zoom detection
    frame_width = cap.shape[2]
    frame_height = cap.shape[1]
    frame_width_center = frame_width/2
    frame_height_center = frame_height/2

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (30,30),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Take first frame and find corners in it
    # ret, old_frame = cap.read()
    # if ret == False:
    #     return -1
    old_frame = cap[0,:,:,:]

    # Find features to track in the first frame
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    
    statics = []
    orientations = []
    zooms = []
    # total_directions = []
    # old_total_directions = []
    for i in range(1,cap.shape[0]):

        directions = []
        norms = []
        movements = []

        # ret,frame = cap.read()
        # if ret == False:
        #     break
        frame = cap[i,:,:,:]

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        if st is None:
            break;

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        # Run through each pair of keypoints (for two concecutive frames) and compute useful metrics 
        for i, (new, old) in enumerate(zip(good_new,good_old)):

            direction, norm, movement = cp_directions(new, old)
            directions.append(direction)
            norms.append(norm)
            movements.append(movement)

        static = change_detection(norms)
        statics.append(static)
        if static == False:
            orientation = orientation_detection(movements, directions)
            orientations.append(orientation)
            if orientation == None:
                zoom = zoom_detection(good_new, good_old, frame_width_center, frame_height_center)
                zooms.append(zoom)

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

    # Compute the sequence max where frame is non static
    max_seq = 0
    for bit, group in itertools.groupby(statics):

        if bit == False:
            max = int(len(list(group)))
            if max > max_seq:
                max_seq = max
    
    # Determine the motion of the camera based on the metrics computed
    all_statics, counts = np.unique(statics, return_counts=True)

    if (max_seq < SEQ_THRESHOLD * len(statics)):
        movement = 'plan fixe'
    else:
        all_orientations, counts = np.unique(orientations, return_counts=True)

        movement = all_orientations[np.argsort(counts)[::-1][0]]

        if movement == None:
            all_zooms, counts = np.unique(zooms, return_counts=True)
            movement = all_zooms[np.argsort(counts)[::-1][0]]

    return movement

# videoname = sys.argv[1]
# cap = cv2.VideoCapture(videoname)
# movement = motion_detection(cap, False)
# print(movement)