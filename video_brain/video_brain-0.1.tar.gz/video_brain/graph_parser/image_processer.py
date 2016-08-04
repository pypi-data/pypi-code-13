import numpy as np
import cv2
import os
import sys
import time

class ImageProcesser():

    def data_augmentation(self, images_targets_iterable, working_directory):

        if not os.path.exists(working_directory + 'database/'):
            os.makedirs(working_directory + 'database/')

        with open(working_directory + 'database/data_transformation.txt', 'w') as report:
            report.write('Flipped Image : True \n')
            report.write('Affine Transformation : True (*2) \n')

        for img, target in images_targets_iterable:

            try:
                flipped_img = cv2.flip(img, 1)

                rows, cols, ch = img.shape
                pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
                pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
                pts3 = np.float32([[200, 200], [70, 70], [200, 50]])
                pts4 = np.float32([[150, 250], [70, 70], [250, 0]])
                M1 = cv2.getAffineTransform(pts1, pts2)
                M2 = cv2.getAffineTransform(pts3, pts4)
                affine_img_1 = cv2.warpAffine(img, M1, (cols, rows))
                affine_img_2 = cv2.warpAffine(img, M2, (cols, rows))

                yield (img, flipped_img, affine_img_1, affine_img_2, target)

            except ValueError:
                pass
                # print(sys.exc_info()[0])
                # print(sys.exc_info()[1])


