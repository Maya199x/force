import numpy as np
import os
import tensorflow as tf

def get_sess(sess=None):
    return tf.get_default_session() if sess is None else sess

def init_sess(sess=None):
    return get_sess(sess).run(tf.global_variables_initializer())

def flatten(tensor, num_leading_axes=1):
    shape = tensor.get_shape().as_list()
    size = np.prod(shape[num_leading_axes:])
    return tf.reshape(tensor, [-1]*num_leading_axes+[size])

def squared_error(x, y):
    return tf.reduce_sum((x - y)**2)

def mean_squared_error(x, y):
    return tf.reduce_mean((x - y)**2)

# Adapted from http://stackoverflow.com/questions/37026425/elegant-way-to-select-one-element-per-row-in-tensorflow
# def selection_slice(matrix, idx, n):
#     # return matrix[tf.range(n),idx]
#     return tf.gather_nd(matrix, tf.transpose(tf.stack([tf.range(n), idx])))

def selection_slice(matrix, idx, unused):
    return tf.reduce_sum(matrix * tf.one_hot(idx, matrix.get_shape()[1]), axis=1)

def periodic_saver(variables, name, period):
    saver = tf.train.Saver(variables)
    def save(engine):
        if engine.global_step % period == 0:
            print('Saving...')
            path = engine.log_path(name)
            saver.save(get_sess(engine.sess), path, global_step=engine.global_step)
    return save
