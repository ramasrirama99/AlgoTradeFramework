import ta
from keras import callbacks
from keras.optimizers import *
from datetime import datetime, timedelta
from sklearn.metrics import classification_report

from algotaf.backend.models.LSTM import lstm
from algotaf.backend.models.CNN import *
from algotaf.backend.experiments.dataproc import process_cnn, process_lstm
from algotaf.backend.db.db_wrapper import get_data_all, connect, get_data_interval


def train_cnn(model, x_train, y_train, x_test, y_test):
    opt = Nadam(lr=0.002)
    opt = Adagrad(lr=0.02)
    # opt = SGD(momentum=0.9)
    ckpt_save = callbacks.ModelCheckpoint('best-cnn.hdf5', save_best_only=True, monitor='val_accuracy', mode='max')
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=25, min_lr=0.000001, verbose=1)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=100, batch_size=64, verbose=1, validation_data=(x_test, y_test),
                        shuffle=True, callbacks=[reduce_lr, ckpt_save])
    y_pred = model.predict_classes(x_test)
    print(classification_report(np.argmax(y_test, axis=1), y_pred))


def train_lstm(model, x_train, y_train, x_test, y_test):
    opt = Adagrad(lr=0.02)
    ckpt_save = callbacks.ModelCheckpoint('best-lstm.hdf5', save_best_only=True, monitor='val_accuracy', mode='max')
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=25, min_lr=0.000001, verbose=1)
    model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])  # Try SGD, adam, adagrad and compare!!!
    model.fit(x_train, y_train, epochs=5, batch_size=1, verbose=2, validation_data=(x_test, y_test), shuffle=False, callbacks=[reduce_lr, ckpt_save])


def print_distribution(data, labels, label_names):
    print(data.shape)
    print(labels.shape)
    for key, val in label_names.items():
        count = labels[labels[:,key] == 1]
        print('{}: {}'.format(val, len(count)))


def main():
    # ticker_list = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
    #                'bp', 'unh', 'cvs', 'tpr']
    ticker_list = ['aapl']
    data = {}
    conn = connect()
    timestamp1 = datetime(2008, 1, 1)
    timestamp2 = datetime(2030, 1, 1)
    window = 50
    num_classes = 4
    dimensions = 1
    label_window = 2
    label_names = {0: 'losses', 1: 'gains', 2: 'both', 3: 'none'}
    for i in ticker_list:
        data[i] = get_data_interval(conn, 'data_daily_{}'.format(i), timestamp1, timestamp2)
    # train, test, label_train, label_test = process_cnn(data, window=window, label_window=label_window)
    train, test, label_train, label_test = process_lstm(data, window=window)
    # print_distribution(train, label_train, label_names)
    # print_distribution(test, label_test, label_names)
    # train_cnn(cnn(input_shape=(window, dimensions), num_classes=num_classes), train, label_train, test, label_test)
    train_lstm(lstm(input_shape=(window, dimensions)), train, label_train, test, label_test)
    # train_lstm(lstm(), train, label_train, test, label_test)


def ta_test():
    ticker_list = ['aapl', 'amzn', 'msft', 'amd', 'nvda', 'goog', 'baba', 'fitb', 'mu', 'fb', 'sq', 'tsm', 'qcom', 'mo',
                   'bp', 'unh', 'cvs', 'tpr']
    data = {}
    conn = connect()
    timestamp1 = datetime(2008, 1, 1)
    timestamp2 = datetime(2030, 1, 1)
    for i in ticker_list:
        data[i] = get_data_interval(conn, 'data_daily_{}'.format(i), timestamp1, timestamp2, pandas=True)
        data[i] = ta.add_all_ta_features(data[i], open='open', high='high', low='low', close='close', volume='volume')
        print(data[i])
    train, test, label_train, label_test = process_data(data)
    print_distribution(train, label_train)
    print_distribution(test, label_test)
    train_cnn(cnn(input_shape=(30, 4), num_classes=num_classes), train, label_train, test, label_test)
    # train_lstm(lstm(), train, label_train, test, label_test)


if __name__ == '__main__':
    main()
    # ta_test()