from keras.layers import *
from keras.models import Sequential, Model
from keras import regularizers


def lcp_recognition_binary_model():
    visible_in = Input(shape=(6000, 1))
    conv_1 = Conv1D(5, kernel_size=5, activation='relu')(visible_in)
    maxpool_1 = MaxPooling1D(pool_size=3, strides=2)(conv_1)

    dropout_1 = Dropout(0.4)(maxpool_1)

    conv_2 = Conv1D(20, kernel_size=5, activation='relu')(dropout_1)
    maxpool_2 = MaxPooling1D(pool_size=3, strides=2)(conv_2)

    conv_3 = Conv1D(32, kernel_size=5, activation='relu')(maxpool_2)
    maxpool_3 = MaxPooling1D(pool_size=3, strides=2)(conv_3)

    flatten = Flatten()(maxpool_3)

    dropout_2 = Dropout(0.5)(flatten)
    dense_1 = Dense(5, activation='relu')(dropout_2)
    dense_2 = Dense(20, activation='relu')(dense_1)
    dense_3 = Dense(80, activation='relu')(dense_2)
    visible_out = Dense(1, activation='sigmoid')(dense_3)

    model = Model(inputs=visible_in, outputs=visible_out)

    print(model.summary())

    return model


def lcp_recognition_binary_model_2():
    '''
    refer Online

    model = Sequential()
    model.add(Conv1D(64, 3, activation='relu', input_shape=(6000, 1)))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(256, 3, activation='relu'))
    model.add(Conv1D(256, 3, activation='relu'))
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    :return:
    '''
    model = Sequential()

    model.add(Conv1D(16, 3, activation='relu', input_shape=(6000, 1)))
    model.add(Dropout(0.3))
    model.add(Conv1D(16, 3, activation='relu'))
    model.add(MaxPooling1D(3, strides=2))

    model.add(Conv1D(32, 3, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Conv1D(32, 3, activation='relu'))
    model.add(MaxPooling1D(3, strides=2))

    model.add(Conv1D(64, 3, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(3, strides=2))

    # model.add(Conv1D(128, 3, activation='relu'))
    # model.add(Dropout(0.3))
    # model.add(Conv1D(128, 3, activation='relu'))
    #
    # model.add(Conv1D(256, 3, activation='relu'))
    # model.add(Dropout(0.3))
    # model.add(Conv1D(256, 3, activation='relu'))

    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    # model.add(LSTM(10, input_length=64))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    print(model.summary())

    return model


def lcp_recognition_binary_model_3():
    visible_in = Input(shape=(6000, 1))

    # Layer 1, part a
    conv_a_1 = Conv1D(64, kernel_size=5, activation='relu')(visible_in)
    drop_a_1 = Dropout(0.3)(conv_a_1)
    conv_a_2 = Conv1D(64, kernel_size=5, activation='relu')(drop_a_1)
    maxpool_a_1 = MaxPooling1D(pool_size=3, strides=2)(conv_a_2)

    conv_a_3 = Conv1D(128, kernel_size=5, activation='relu')(maxpool_a_1)
    drop_a_2 = Dropout(0.3)(conv_a_3)
    conv_a_4 = Conv1D(128, kernel_size=5, activation='relu')(drop_a_2)
    maxpool_a_2 = MaxPooling1D(pool_size=3, strides=2)(conv_a_4)

    gap_a_1 = GlobalAveragePooling1D()(maxpool_a_2)

    # Layer 1, part b
    conv_b_1 = Conv1D(64, kernel_size=5, activation='relu')(visible_in)
    drop_b_1 = Dropout(0.3)(conv_b_1)
    conv_b_2 = Conv1D(64, kernel_size=5, activation='relu')(drop_b_1)
    maxpool_b_1 = MaxPooling1D(pool_size=3, strides=2)(conv_b_2)

    conv_b_3 = Conv1D(128, kernel_size=5, activation='relu')(maxpool_b_1)
    drop_b_2 = Dropout(0.3)(conv_b_3)
    conv_b_4 = Conv1D(128, kernel_size=5, activation='relu')(drop_b_2)
    maxpool_b_2 = MaxPooling1D(pool_size=3, strides=2)(conv_b_4)

    gap_b_1 = GlobalAveragePooling1D()(maxpool_b_2)

    # Layer 2
    merge_1 = concatenate([gap_a_1, gap_b_1])
    dense_1 = Dense(50, activation='relu')(merge_1)
    drop_2 = Dropout(0.2)(dense_1)
    visible_out = Dense(1, activation='sigmoid')(drop_2)

    model = Model(inputs=visible_in, outputs=visible_out)

    print(model.summary())

    return model


# TESTING AT LAPTOP
def model_1():
    visible_in = Input(shape=(6000, 1))

    conv_1 = Conv1D(filters=32, kernel_size=5, strides=1, activation='relu', name='Conv_a_1')(visible_in)
    gap = GlobalAveragePooling1D()(conv_1)
    visible_out = Dense(1, activation='sigmoid')(gap)

    model = Model(inputs=visible_in, outputs=visible_out)

    print(model.summary())

# lcp_recognition_binary_model_3()

model_1()