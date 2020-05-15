# 
# Copyright (C) 2002-2019 Igor Sysoev
# Copyright (C) 2011,2019 Nginx, Inc.
# Copyright (C) 2010-2019 Alibaba Group Holding Limited
# Copyright (C) 2011-2013 Xiaozhe "chaoslawful" Wang
# Copyright (C) 2011-2013 Zhang "agentzh" Yichun
# Copyright (C) 2011-2013 Weibin Yao
# Copyright (C) 2012-2013 Sogou, Inc.
# Copyright (C) 2012-2013 NetEase, Inc.
# Copyright (C) 2014-2017 Intel, Inc.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#  
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#   OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#   LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#   OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#   SUCH DAMAGE.
#  

import tensorflow as tf

def dice(_x, axis=-1, epsilon=0.000000001, name=''):
  with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
    alphas = tf.get_variable('alpha'+name, _x.get_shape()[-1],                                  
                         initializer=tf.constant_initializer(0.0),                         
                         dtype=tf.float32)
    beta = tf.get_variable('beta'+name, _x.get_shape()[-1],                                  
                         initializer=tf.constant_initializer(0.0),                         
                         dtype=tf.float32)
  input_shape = list(_x.get_shape())

  reduction_axes = list(range(len(input_shape)))
  del reduction_axes[axis]
  broadcast_shape = [1] * len(input_shape)
  broadcast_shape[axis] = input_shape[axis]
                                                                                                                                                                            
  # case: train mode (uses stats of the current batch)
  mean = tf.reduce_mean(_x, axis=reduction_axes)
  brodcast_mean = tf.reshape(mean, broadcast_shape)
  std = tf.reduce_mean(tf.square(_x - brodcast_mean) + epsilon, axis=reduction_axes)
  std = tf.sqrt(std)
  brodcast_std = tf.reshape(std, broadcast_shape)
  x_normed = tf.layers.batch_normalization(_x, center=False, scale=False, name=name, reuse=tf.AUTO_REUSE)
  # x_normed = (_x - brodcast_mean) / (brodcast_std + epsilon)
  x_p = tf.sigmoid(beta * x_normed)
 
  
  return alphas * (1.0 - x_p) * _x + x_p * _x

def parametric_relu(_x):
  with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
    alphas = tf.get_variable('alpha', _x.get_shape()[-1],
                         initializer=tf.constant_initializer(0.0),
                         dtype=tf.float32)
  pos = tf.nn.relu(_x)
  neg = alphas * (_x - abs(_x)) * 0.5

  return pos + neg
