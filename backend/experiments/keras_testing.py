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
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
import sklearn


class Database:
    def __init__(self):
        try:
            with open('fileio/sensitive_data.txt') as sensitive:
                user = sensitive.readline().strip()
                password = sensitive.readline().strip()
            with open('fileio/db_host.txt') as host:
                hostname = host.readline().strip()
            self.conn = psycopg2.connect('dbname=algotaf user=' + user + ' password=' + password + ' host=' + hostname)
        except Exception as error:
            print(str(error))

    def select_data(self, tablename, columns):
        cur = self.conn.cursor()
        cur.execute(sql.SQL('SELECT') + sql.SQL(', ').join(sql.Identifier(i) for i in columns) + sql.SQL('FROM {};').format(sql.Identifier(tablename)))
        return cur.fetchall()


try:
    db = Database()
    data = db.select_data('data_daily_aapl', ['date', 'open', 'high', 'low', 'close', 'dividend', 'split_coefficient'])
    date = []
    close = []
    for i in data:
        date.append(i[0])
        close.append(i[4])
    for i in range(len(date)):
        date[i] = datetime.strptime(date[i], '%Y-%m-%d')
    date = dates.date2num(date)
except Exception as error:
    print(str(error))

# try:
    # plt.plot_date(date, close, linestyle='solid', markersize=0)
    # plt.show()
# except Exception as error:
#     print(str(error))
try:
    Y_binary = utils.to_categorical(close)
    split = int(len(date) * 0.9)
    X_train = date[0:split - 1]
    X_test = date[split:len(date) - 1]
    Y_train = Y_binary[0:split - 1]
    Y_test = Y_binary[split:len(close) - 1]

    model = models.Sequential()
    model.add(layers.Dense(64, input_dim=703, activity_regularizer=regularizers.l2(0.01)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(16, activity_regularizer=regularizers.l2(0.01)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Dense(1))
    model.add(layers.Activation('softmax'))
    opt = optimizers.Nadam(lr=0.002)
    # model = models.Sequential()
    # model.add(layers.Dense(64, input_dim=1))
    # model.add(layers.BatchNormalization())
    # model.add(layers.LeakyReLU())
    # model.add(layers.Dense(703))
    # model.add(layers.Activation('softmax'))
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=5, min_lr=0.000001, verbose=1)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(Y_train, X_train, epochs=50, batch_size=128, verbose=1, validation_data=(Y_test, X_test), shuffle=True, callbacks=[reduce_lr])
    # plt.figure()
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='best')
    # plt.show()

    pred = model.predict(np.array(Y_test))
    original = Y_test
    predicted = pred
    plt.plot(original, color='black', label='Original data')
    plt.plot(predicted, color='blue', label='Predicted data')
    plt.legend(loc='best')
    plt.title('Actual and predicted')
    plt.show()

except Exception as error:
    print(str(error))