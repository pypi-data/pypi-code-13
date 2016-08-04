import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


def cluster_video(cap):
    # Initiate ORB detector
    orb = cv2.ORB(edgeThreshold=15, patchSize=31, nlevels=8, scaleFactor=1.2,
                         WTA_K=2, scoreType=cv2.ORB_HARRIS_SCORE, firstLevel=0, nfeatures=400)

    frames = []
    features = []
    for i in range(1, cap.shape[0]):

        frame = cap[i, :, :, :]
        # ret, frame = cap.read()
        # if ret == True:

        # find the keypoints with ORB
        kp = orb.detect(frame, None)

        # compute the descriptors with ORB
        kp, des = orb.compute(frame, kp)

        if len(kp) != 0:
            if des.shape[0] == 400:
                des = np.float32(des)
                features.append(des)
                frames.append(frame)

    features = np.array(features)
    frames = np.array(frames)

    # print(features.shape)

    if features.shape[0] > 50:

        # define criteria and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        # ret, labels, centers = cv2.kmeans(features, 2, [], criteria, 200, 0, flags)
        ret, labels, centers = cv2.kmeans(features, 2, criteria, 10, flags)

        features = np.reshape(features, (features.shape[0], features.shape[1] * features.shape[2]))

        best_frames = []

        Y = cdist(features, centers, 'euclidean')
        Y0 = Y[:, 0]
        Y1 = Y[:, 1]

        frame = frames[np.argsort(Y0)[0], :, :]
        best_frames.append(frame)

        frame = frames[np.argsort(Y1)[0], :, :]
        best_frames.append(frame)

    else:
        best_frames = []

    return best_frames

    # videoname = sys.argv[1]
    # cap = cv2.VideoCapture(videoname)
    # best_frames = cluster_video(cap)

    # for frame in best_frames:
    # 	plt.imshow(frame), plt.show()
