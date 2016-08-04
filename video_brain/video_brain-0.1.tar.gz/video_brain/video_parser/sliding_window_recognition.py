# import the necessary packages
from skimage.transform import pyramid_gaussian
import argparse
import cv2
import time
import imutils
import numpy as np
import matplotlib.pyplot as plt
import sys


def pyramid(image, scale=1.5, minSize=(30, 30)):
    # Resizing + Gaussian smoothing.
    for (i, resized) in enumerate(pyramid_gaussian(image, downscale=scale)):
        # if the image is too small, break from the loop
        if resized.shape[0] < 30 or resized.shape[1] < 30:
            break

        yield resized


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-s", "--scale", type=float, default=1.5, help="scale factor size")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
(winW, winH) = (128, 128)

orb = cv2.ORB()

# loop over the image pyramid
for resized in pyramid(image, scale=1.5):
    # loop over the sliding window for each layer of the pyramid
    for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue

        mask = np.zeros((resized.shape[0], resized.shape[1]), dtype=np.uint8)
        # mask.fill(0)
        mask[x:(x + winW), y:(y + winH)] = 1

        converted_resized = (resized * 255).astype(np.uint8)

        kp = orb.detect(converted_resized, mask)

        # compute the descriptors with ORB
        kp, des = orb.compute(converted_resized, kp)

    # clone = resized.copy()
    # cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
    # cv2.imshow("Window", clone)
    # cv2.waitKey(1)
    # time.sleep(0.025)

    # img2 = cv2.drawKeypoints(converted_resized,kp,color=(0,255,0), flags=0)
    # plt.imshow(img2),plt.show()

    # since we do not have a classifier, we'll just draw the window
