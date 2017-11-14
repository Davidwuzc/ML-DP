#!/usr/bin/python
#-*- coding:utf-8 -*
###########################
#File Name: network_in_network.py
#Author: gegey2008
#Mail: milkyang2008@126.com
#Created Time: 2017-11-13 21:08:24
############################

"""
Applying 'Network IN Network' to CIFAR-10 classification task.

References:
    Network IN Network. Min Li, Qiang Chen & Shuicheng Yan, 2014

Links:
    http://arxiv.org/pdf/1312.4400v3.pdf

"""


from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.estimator import regression

#Data loading and preprocessing
from tflearn.datasets import cifar10
(X, Y), (X_test, Y_test) = cifar10.load_data()
#X, Y = shuffle(X, Y)
Y = to_categorical(Y, 10)
Y_test = to_categorical(Y_test, 10)

# Building 'Network In Network'
network = input_data(shape=[None, 32, 32, 3])
network = conv_2d(network, 192, 5, activation='relu')
network = conv_2d(network, 160, 1, activation='relu')
network = conv_2d(network, 96, 1, activation='relu')
network = max_pool_2d(network, 3, strides=2)
network = dropout(network, 0.5)
network = conv_2d(network, 192, 5, activation='relu')
network = conv_2d(network, 192, 1, activation='relu')
network = conv_2d(network, 192, 1, activation='relu')
network = avg_pool_2d(network, 3, strides=2)
network = dropout(network, 0.5)
network = conv_2d(network, 192, 3, activation='relu')
network = conv_2d(network, 192, 1, activation='relu')
network = conv_2d(network, 10, 1, activation='relu')
network = avg_pool_2d(network, 8)
network = flatten(network)
network = regression(network, optimizer='adam',
                    loss='softmax_categorical_crossentropy',
                    learning_rate=0.001)

#Training
model = tflearn.DNN(network)
model.fit(X, Y, n_epoch=50, shffle=False, validation_set=(X_test, Y_test),
         show_metric=True, batch_size=128, run_id='cifar10_net_in_net')
