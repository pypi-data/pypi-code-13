import MySQLdb as mdb
import numpy as np
import matplotlib.pyplot as plt
import sys

caffe_root = '/home/leo/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')
import caffe
import glob
import os


def init_network(model_name):
    # set display defaults
    plt.rcParams['figure.figsize'] = (10, 10)  # large images
    plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
    plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

    caffe.set_mode_gpu()

    model_def = caffe_root + 'resources/' + str(model_name) + '/deploy.prototxt'
    model_weights = caffe_root + 'resources/' + str(model_name) + '/' + str(model_name) + '.caffemodel'

    net = caffe.Net(model_def,  # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)  # use test mode (e.g., don't perform dropout)

    # load the mean ImageNet image (as distributed with Caffe) for subtraction
    # mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
    # mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
    # print 'mean-subtracted values:', zip('BGR', mu)

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost dimension
    # transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

    # set the size of the input (we can skip this if we're happy
    #  with the default; we can also change it later, e.g., for different batch sizes)

    if model_name.endswith('caffenet'):
        net.blobs['data'].reshape(1,  # batch size
                                  3,  # 3-channel (BGR) images
                                  227, 227)  # image size is 227x227
    elif model_name.endswith('network'):
        net.blobs['data'].reshape(50,  # batch size
                                  3,  # 3-channel (BGR) images
                                  224, 224)  # image size is 227x227

    return net, transformer


def net_features(model_name):
    con = mdb.connect('localhost', 'leo', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
    cur = con.cursor()

    net, transformer = init_network(model_name)

    imagenames = glob.glob('../../../images/*')

    for imagename in imagenames:
        media_ref = imagename.split('/')[-1].split('.')[0].split('_')[0]
        name = imagename.split('/')[-1].split('.')[0]

        # cur.execute('SELECT media FROM features WHERE imagename = %s', \
        # 			 (name,) )

        # media = cur.fetchone()

        # if media is None:

        image = caffe.io.load_image(imagename)

        transformed_image = transformer.preprocess('data', image)

        # copy the image data into the memory allocated for the net
        net.blobs['data'].data[...] = transformed_image

        ### perform classification
        output = net.forward()
        last_feats = net.blobs['loss3/classifier'].data

        features = last_feats[0, :]

        # print(np.array(features).shape)

        cur.execute('UPDATE features SET vgg_features = %s WHERE imagename = %s', (str(features), name))
        con.commit()


def more_net_features(model_name):
    con = mdb.connect('localhost', 'leo', 'castor69', 'webcastor', charset='utf8', use_unicode=True)
    cur = con.cursor()

    net, transformer = init_network(model_name)

    imagenames = []
    for root, dirnames, filenames in os.walk('../../more_images'):

        for dirname in dirnames:
            names = glob.glob('../../more_images/' + dirname + '/*')
            imagenames = imagenames + names

    for imagename in imagenames:

        media_ref = imagename.split('/')[-1].split('.')[0].split('_')[0]
        name = imagename.split('/')[-1].split('.')[0]

        cur.execute('SELECT media FROM features WHERE imagename = %s', \
                    (name,))

        media = cur.fetchone()

        if media is None:
            image = caffe.io.load_image(imagename)
            transformed_image = transformer.preprocess('data', image)

            # copy the image data into the memory allocated for the net
            net.blobs['data'].data[...] = transformed_image

            ### perform classification
            output = net.forward()

            last_feats = net.blobs['fc8'].data

            features = last_feats[0, :]

            cur.execute('INSERT INTO features (caffe_features, media, imagename, more_images) VALUES (%s, %s, %s, %s)', \
                        (str(features), media_ref, name, 1))
            con.commit()

# model_name = sys.argv[1]
# print(model_name)
# net_features(model_name)
# more_net_features()
