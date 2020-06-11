from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM


def lstm(filters=32, input_shape=None, dropout=0.2):
    model = Sequential()
    model.add(LSTM(filters, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(dropout))
    model.add(LSTM(int(filters / 2)))
    model.add(Dropout(dropout))
    model.add(Dense(1))
    model.add(Activation('linear'))
    return model