from keras.models import *
from keras.layers import *


def cnn(filters=64, num_classes=4, input_shape=None, dropout=0.05):
    encoder = Sequential()
    encoder.add(Conv1D(filters, 3, padding='same', activation='relu', input_shape=input_shape))
    encoder.add(BatchNormalization())
    encoder.add(SpatialDropout1D(dropout))
    encoder.add(MaxPool1D(4, 4, padding='same'))

    encoder.add(Conv1D(2*filters, 3, padding='same', activation='relu'))
    encoder.add(BatchNormalization())
    encoder.add(SpatialDropout1D(dropout))
    encoder.add(MaxPool1D(padding='same'))

    encoder.add(Conv1D(3 * filters, 3, padding='same', activation='relu'))
    encoder.add(BatchNormalization())
    encoder.add(SpatialDropout1D(dropout))
    encoder.add(MaxPool1D(padding='same'))

    encoder.add(Conv1D(4 * filters, 3, padding='same', activation='relu'))
    encoder.add(BatchNormalization())
    encoder.add(SpatialDropout1D(dropout))
    encoder.add(MaxPool1D(padding='same'))

    encoder.add(GlobalMaxPool1D())

    encoder.add(Dense(num_classes, activation='softmax'))

    return encoder


def simple(filters=64, num_classes=4, input_shape=None, dropout=0.5):
    model = Sequential()
    model.add(Conv1D(filters, 4, activation='relu', input_shape=input_shape))
    model.add(Conv1D(filters, 4, activation='relu'))
    model.add(Dropout(dropout))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    return model


def simple_stream(filters=64, num_classes=1, input_shape=None, dropout=0.5):
    model = Sequential()
    model.add(Conv1D(filters, 2, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(num_classes))
    return model


def alexnet(filters=64, num_classes=4, input_shape=None, dropout=0.4):
    model = Sequential()
    # 1st Convolutional Layer
    model.add(Conv1D(filters=96, input_shape=input_shape, kernel_size=11, padding='same', activation='relu'))
    # model.add(Activation('relu'))
    # Max Pooling
    model.add(MaxPooling1D(pool_size=2, padding='same'))
    # 2nd Convolutional Layer
    model.add(Conv1D(filters=256, kernel_size=11, padding='same', activation='relu'))
    # model.add(Activation('relu'))
    # Max Pooling
    model.add(MaxPooling1D(pool_size=2, padding='same'))
    # 3rd Convolutional Layer
    model.add(Conv1D(filters=384, kernel_size=3, padding='same', activation='relu'))
    # model.add(Activation('relu'))
    # 4th Convolutional Layer
    model.add(Conv1D(filters=384, kernel_size=3, padding='same', activation='relu'))
    # model.add(Activation('relu'))
    # 5th Convolutional Layer
    model.add(Conv1D(filters=256, kernel_size=3, padding='same', activation='relu'))
    # model.add(Activation('relu'))
    # Max Pooling
    model.add(MaxPooling1D(pool_size=2, padding='same'))
    # Passing it to a Fully Connected layer
    model.add(Flatten())
    # 1st Fully Connected Layer
    model.add(Dense(4096, input_shape=input_shape, activation='relu'))
    # model.add(Activation('relu'))
    # Add Dropout to prevent overfitting
    model.add(Dropout(dropout))
    # 2nd Fully Connected Layer
    model.add(Dense(4096, activation='relu'))
    # model.add(Activation('relu'))
    # Add Dropout
    model.add(Dropout(dropout))
    # 3rd Fully Connected Layer
    model.add(Dense(num_classes, activation='softmax'))
    # model.add(Activation('relu'))
    # Add Dropout
    # model.add(Dropout(dropout))
    # Output Layer
    # model.add(Dense(17))
    # model.add(Activation(‘softmax’))
    return model


def unet(filters=64, num_classes=4, input_shape=None, dropout=0.5):
    inputs = Input(input_shape)
    conv1 = Conv1D(filters, 4, padding='same', activation='relu', kernel_initializer='he_normal')(inputs)
    conv1 = Conv1D(filters, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling1D(pool_size=2)(conv1)
    conv2 = Conv1D(filters*2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(pool1)
    conv2 = Conv1D(filters*2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv2)
    pool2 = MaxPooling1D(pool_size=2)(conv2)
    conv3 = Conv1D(filters*4, 4, padding='same', activation='relu', kernel_initializer='he_normal')(pool2)
    conv3 = Conv1D(filters*4, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv3)
    pool3 = MaxPooling1D(pool_size=2)(conv3)
    conv4 = Conv1D(filters*8, 4, padding='same', activation='relu', kernel_initializer='he_normal')(pool3)
    conv4 = Conv1D(filters*8, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv4)
    drop4 = Dropout(dropout)(conv4)
    pool4 = MaxPooling1D(pool_size=2)(drop4)

    conv5 = Conv1D(filters*16, 4, padding='same', activation='relu', kernel_initializer='he_normal')(pool4)
    conv5 = Conv1D(filters*16, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv5)
    drop5 = Dropout(dropout)(conv5)

    up6 = Conv1D(filters*8, 4, padding='same', activation='relu', kernel_initializer='he_normal')(UpSampling1D(size=2)(drop5))
    merge6 = concatenate([drop4, up6], axis=3)
    conv6 = Conv1D(filters*8, 4, padding='same', activation='relu', kernel_initializer='he_normal')(merge6)
    conv6 = Conv1D(filters*8, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv6)

    up7 = Conv1D(filters*4, 4, padding='same', activation='relu', kernel_initializer='he_normal')(UpSampling1D(size=2)(conv6))
    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv1D(filters*4, 4, padding='same', activation='relu', kernel_initializer='he_normal')(merge7)
    conv7 = Conv1D(filters*4, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv7)

    up8 = Conv1D(filters*2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(UpSampling1D(size=2)(conv7))
    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv1D(filters*2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(merge8)
    conv8 = Conv1D(filters*2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv8)

    up9 = Conv1D(filters, 4, padding='same', activation='relu', kernel_initializer='he_normal')(UpSampling1D(size=2)(conv8))
    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv1D(filters, 4, padding='same', activation='relu', kernel_initializer='he_normal')(merge9)
    conv9 = Conv1D(filters, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv9 = Conv1D(2, 4, padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv10 = Conv1D(1, 1, padding='same', activation='sigmoid', kernel_initializer='he_normal')(conv9)

    model = Model(input=inputs, output=conv10)