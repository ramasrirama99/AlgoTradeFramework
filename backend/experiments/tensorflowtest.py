import sqlalchemy
from sqlalchemy import select
import psycopg2
from psycopg2 import sql
import pandas as pd
from backend import config
from backend.fileio import apikey
import alpha_vantage
from pprint import pprint
from alpha_vantage.timeseries import TimeSeries
from tensorflow.keras import models, layers, callbacks, optimizers, utils, regularizers
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
import sklearn
import tensorflow as tf
import random

# x = tf.Variable(3, name='x')
# y = tf.Variable(4, name='y')
# f = x * x * y + y + 2
# # sess = tf.Session()
# # sess.run(x.initializer)
# # sess.run(y.initializer)
# # result = sess.run(f)
# init = tf.global_variables_initializer()
# with tf.Session() as sess:
#     init.run()
#     result = f.eval()
# print(result)
# sess.close()
#
# x1 = tf.Variable(1)
# x1.graph is tf.get_default_graph()
# graph = tf.Graph()
# with graph.as_default():
#     x2 = tf.Variable(2)
# x2.graph is graph

w = tf.constant(3)
x = w + 2
y = x + 5
z = x * 3
with tf.Session() as sess:
    print(y.eval())
    print(x.eval())