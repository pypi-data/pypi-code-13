from motion_detection import motion_detection
from clustering import cluster_video
import matplotlib.pyplot as plt
import sys
import cv2
import glob
import logging
import skvideo.io

# logging.basicConfig(filename='../logs/key_frames_log.txt', level=logging.DEBUG)
from skvideo.io import vread

def extract_key_frames(videoname):

    # cap = cv2.VideoCapture(videoname)
    ext = videoname.split('.')[-1]

    # if ext == 'f4v' or ext == 'mp4':

    try:
        cap = vread(videoname, backend='libav')

    except RuntimeError:
        print('Runtime Error')

        # try:
        #     movement = motion_detection(cap)
        # except:
        #     movement = ''
        #     logging.exception('motion detection : ' + str(videoname))

        # if movement == 'plan fixe':

    key_frames = []

    # nb_frames = cap.get(7)
    nb_frames = cap.shape[0]

    # cap.set(1,int(nb_frames/3))
    # ret, frame = cap.read()
    frame = cap[int(nb_frames / 3), :, :, :]
    key_frames.append(frame)

    # cap.set(1,(2*nb_frames)/3)
    # ret, frame = cap.read()
    frame = cap[int((2 * nb_frames) / 3), :, :, :]
    key_frames.append(frame)

        # else:

            # key_frames = []
            # cap.set(1,0)
            # try:
            #     key_frames = cluster_video(cap)
            # except:
            #     logging.exception('cluster video : ' + str(videoname))
    # else:
    #     key_frames = []

    # cv2.destroyAllWindows()
    # cap.release()

    return key_frames


def get_key_frames(rushnames):

    videos = []
    for rushname in rushnames:
        key_frames = extract_key_frames(rushname)
        videos.append(key_frames)

    return videos


def process_specific_frames():
    rushs_frames = get_key_frames(sys.argv[1:])


# write_frames(rushs_frames, sys.argv[1:])

def process_all_frames():
    videonames = glob.glob('../../../rushs/*')

    all_images = glob.glob('../../../images/*')
    all_images = [name.split('/')[-1].split('.')[0].split('_')[0] for name in all_images]

    key_frames = []

    for videoname in videonames:

        name = videoname.split('/')[-1].split('.')[0].split('_')[0]

        if name not in all_images:
            rushs_frames = get_key_frames([videoname])
            write_frames(rushs_frames, [videoname])
        # key_frames.append(rushs_frames)

    return key_frames


def write_frames(rushs_frames, videonames):
    for rush, name in zip(rushs_frames, videonames):
        name = name.split('/')[-1].split('.')[0].split('_')[0]
        for i, frame in enumerate(rush):
            # plt.imshow(frame), plt.show()
            cv2.imwrite('../../../images/rushs/' + name + '_' + str(i) + '.png', frame)

# process_specific_frames()
# process_all_frames()
