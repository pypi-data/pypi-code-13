# -*- coding: utf-8 -*-
import sugartensor as tf
import matplotlib.pyplot as plt

# set log level to debug
tf.sg_verbosity(10)

#
# inputs
#

batch_size = 100
num_category = 10

# target_number
target_num = tf.sg_input()
# target_cval_1 = tf.constant(0.5, dtype=tf.sg_floatx)
# target_cval_2 = tf.constant(0.5, dtype=tf.sg_floatx)

# category variables
z_cat = (tf.ones(batch_size, dtype=tf.sg_intx) * target_num).sg_one_hot(depth=num_category)

# random seed = categorical variable + continous variable + random uniform
z = z_cat.sg_concat(target=tf.random_uniform((batch_size, 90)))


#
# create generator
#

# generator network
with tf.sg_context(name='generator', stride=2, act='relu', bn=True):
    gen = (z.sg_dense(dim=1024)
           .sg_dense(dim=7*7*128)
           .sg_reshape(shape=(-1, 7, 7, 128))
           .sg_upconv(size=4, dim=64)
           .sg_upconv(size=4, dim=1, act='sigmoid', bn=False).sg_squeeze())

with tf.Session() as sess:
    tf.sg_init(sess)
    # restore parameters
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('asset/train/infogan/ckpt'))
    imgs = sess.run(gen)
    plt.imshow(imgs[0], 'gray')
    print imgs.shape
