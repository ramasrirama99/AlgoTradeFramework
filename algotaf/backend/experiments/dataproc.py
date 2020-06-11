import random
import ta
import numpy as np
from datetime import datetime
from keras.utils.np_utils import to_categorical


def aroon(data, window=30):
    aroon_up = []
    aroon_down = []
    for i, val in enumerate(data):
        index = window + i
        if index < len(data):
            cur = data[i : index][:,1]
            up = np.argmax(cur)
            aroon_up.append((up/window) * 100)

    for i, val in enumerate(data):
        index = window + i
        if index < len(data):
            cur = data[i : index][:,2]
            down = np.argmin(cur)
            aroon_down.append((down/window) * 100)

    return np.asarray(aroon_up), np.asarray(aroon_down)


def sma(data, window=30):
    moving_avg = []
    for i, val in enumerate(data):
        index = window + i
        if index < len(data):
            cur = data[i : index][:,3]
            mean = np.mean(cur)
            moving_avg.append(mean)
    return np.asarray(moving_avg)


def ema(data, window=30):
    moving_avg = []
    initial = sma(data, window=window)
    multiplier = (2 / (window + 1))
    previous_ema = initial[0]
    for i, val in enumerate(data):
        index = window + i
        if index < len(data):
            close = data[index][3]
            cur_ema = (close - previous_ema) * multiplier + previous_ema
            moving_avg.append(cur_ema)
            previous_ema = cur_ema
    return np.asarray(moving_avg)


def macd(data):
    ema26 = ema(data, window=26)
    ema12 = ema(data, window=12)[14:]
    moving_avg = ema26 - ema12
    return np.asarray(moving_avg)


def rsi(data, window=14):
    moving_avg = []
    prev_gain = 0
    prev_loss = 0
    for i, val in enumerate(data):
        index = window + i
        if index < len(data):
            cur = data[i : index][:,3]
            close = data[index][3]
            avg_gain = np.mean(np.argwhere(cur >= close))
            avg_loss = np.mean(np.argwhere(cur < close))
            gain_step = (prev_gain * (window - 1)) + avg_gain
            loss_step = (prev_loss * (window - 1)) + avg_loss
            step = 100 - (100 / (1 + (gain_step / loss_step)))
            moving_avg.append(step)
            prev_gain = avg_gain
            prev_loss = avg_loss
    return np.asarray(moving_avg)


# def adx()


# def vwap(data): Use for intraday polygon data


def process_cnn(dataset, window=30, label_window=10, train_split=0.6, mode='daily_ohlcv', split_type='date', label_type='label_binary'):
    train_set = []
    test_set = []
    label_train = []
    label_test = []

    if mode == 'daily_ohlcv':
        indices = [1,2,3,4,6]
    elif mode == 'intraday_tohlcv':
        indices = [1,2,3,4]
    else:
        print('Error: Invalid Mode')
        return

    if split_type == 'date':
        print('Processing: Date mode')

        for ticker, data in dataset.items():
            print('Ticker: {}, Size: {}'.format(ticker, len(data)))

            train_split_index = int(len(data) * train_split)

            train = np.asarray(data[0:train_split_index])[:,indices]
            test = np.asarray(data[train_split_index:len(data)])[:,indices]
            all_prices = np.asarray(data)[:,indices]

            # data_sma = sma(all_prices)
            # print(data_sma.shape)
            # data_aroon_up, data_aroon_down = aroon(all_prices)
            # print(data_aroon_up.shape)
            # print(data_aroon_down.shape)
            # data_ema = ema(all_prices)
            # print(data_ema.shape)
            # data_macd = macd(all_prices)
            # print(data_macd.shape)
            # data_rsi = rsi(all_prices)
            # print(data_rsi.shape)
            # print('data')
            # print(all_prices[:60][:,3])
            # print('sma')
            # print(data_sma[:30])
            # print('aroon up')
            # print(data_aroon_up[:30])
            # print('aroon_down')
            # print(data_aroon_down[:30])
            # print('ema')
            # print(data_ema[:30])
            # print('macd')
            # print(data_macd[:30])
            # print('rsi')
            # print(data_rsi[:30])

            train_data, train_label = iterate_window(train, 0, all_prices, window, label_window, label_type)
            test_data, test_label = iterate_window(test, len(train), all_prices, window, label_window, label_type)
            train_set.extend(train_data)
            test_set.extend(test_data)
            label_train.extend(train_label)
            label_test.extend(test_label)

    elif split_type == 'stock':
        print('Processing: Stock mode')

        tickers = list(dataset)
        random.shuffle(tickers)
        train_split_index = int(len(tickers) * train_split)

        train = tickers[0 : train_split_index]
        test = tickers[train_split_index : len(tickers)]

        for ticker, data in dataset.items():
            print('Ticker: {}, Size: {}'.format(ticker, len(data)))
            all_prices = np.asarray(data)[:,indices]
            if ticker in train:
                label_train.extend(iterate_window(all_prices, 0, all_prices, window, label_window))
            elif ticker in test:
                label_test.extend(iterate_window(all_prices, 0, all_prices, window, label_window))
            else:
                print('Error: Indexing Tickers')
                return

    else:
        print('Error: Invalid Mode')
        return

    return np.squeeze(np.asarray(train_set))[:,:,[3]], np.squeeze(np.asarray(test_set))[:,:,[3]], to_categorical(label_train), to_categorical(label_test)


def process_lstm(dataset, window=30, train_split=0.8, mode='daily_ohlcv'):
    train_set = []
    test_set = []
    label_train = []
    label_test = []

    if mode == 'daily_ohlcv':
        indices = [0,1,2,3,4,6]
    elif mode == 'intraday_tohlcv':
        indices = [1,2,3,4]
    else:
        print('Error: Invalid Mode')
        return

    for ticker, data in dataset.items():
        print('Ticker: {}, Size: {}'.format(ticker, len(data)))

        train_split_index = int(len(data) * train_split)

        train = np.asarray(data[0:train_split_index])[:,indices]
        test = np.asarray(data[train_split_index:len(data)])[:,indices]
        all_prices = np.asarray(data)[:,indices]

        train_data, train_label = iterate_window(train, 0, all_prices, window, 0, label_type='label_time')
        test_data, test_label = iterate_window(test, len(train), all_prices, window, 0, label_type='label_time')
        train_set.extend(train_data)
        test_set.extend(test_data)
        label_train.extend(train_label)
        label_test.extend(test_label)

    return np.squeeze(np.asarray(train_set))[:,:,[3]], np.squeeze(np.asarray(test_set))[:,:,[3]], np.asarray(label_train), np.asarray(label_test)


def iterate_window(data, train_len, all_prices, window, label_window, label_type):
    data_set = []
    label_set = []
    for i, val in enumerate(data):
        cur = i + window
        end = cur + label_window
        if cur < len(data):
            window_data = data[i: cur]
            data_set.append(window_data)
            if label_type == 'label_binary':
                label = label_binary(train_len + cur, train_len + end, all_prices)
            elif label_type == 'label_time':
                label = label_time(cur, data)
            else:
                label = label_jumps(train_len + cur, train_len + end, all_prices)
            label_set.append(label)
    return data_set, label_set


def label_time(cur, data):
    date = data[:,0][cur]
    return datetime(date.year, date.month, date.day).timestamp()


def label_jumps(cur, end, data, threshold=0.05):
    current_price = data[:,3][cur]
    loss_price = current_price * (1 - threshold)
    gain_price = current_price * (1 + threshold)
    gains = 0
    losses = 0
    for j in range(cur, end):
        if data[:,1][j] >= gain_price:
            gains += 1
        if data[:,2][j] <= loss_price:
            losses += 1
    if gains > 0 and losses > 0:
        return 3
    elif gains > 0:
        return 2
    elif losses > 0:
        return 0
    else:
        return 1


def label_binary(cur, end, data):
    current_price = data[:,3][cur]
    gains = 0
    losses = 0
    for j in range(cur, end):
        if data[:,3][j] > current_price:
            gains += 1
        if data[:,3][j] < current_price:
            losses += 1
    if gains > 0 and losses > 0:
        return 2
    elif gains > 0:
        return 1
    elif losses > 0:
        return 0
    else:
        return 3


def label_runs(cur, end, data, threshold=0.05):
    current_price = data[:,3][cur]
    loss_price = current_price * (1 - threshold)
    gain_price = current_price * (1 + threshold)
    gains = 0
    losses = 0
    for j in range(cur, end):
        if data[:,1][j] >= gain_price:
            gains += 1
        if data[:,2][j] <= loss_price:
            losses += 1
    if gains > 0 and losses > 0:
        return 3
    elif gains > 0:
        return 2
    elif losses > 0:
        return 0
    else:
        return 1


def label_peaks(cur, end, data, threshold=0.05):
    current_price = data[:,3][cur]
    loss_price = current_price * (1 - threshold)
    gain_price = current_price * (1 + threshold)
    gains = 0
    losses = 0
    for j in range(cur, end):
        if data[:,1][j] >= gain_price:
            gains += 1
        if data[:,2][j] <= loss_price:
            losses += 1
    if gains > 0 and losses > 0:
        return 3
    elif gains > 0:
        return 2
    elif losses > 0:
        return 0
    else:
        return 1


def label_volatility(cur, end, data, threshold=0.05):
    current_price = data[:,3][cur]
    loss_price = current_price * (1 - threshold)
    gain_price = current_price * (1 + threshold)
    gains = 0
    losses = 0
    for j in range(cur, end):
        if data[:,1][j] >= gain_price:
            gains += 1
        if data[:,2][j] <= loss_price:
            losses += 1
    if gains > 0 and losses > 0:
        return 3
    elif gains > 0:
        return 2
    elif losses > 0:
        return 0
    else:
        return 1