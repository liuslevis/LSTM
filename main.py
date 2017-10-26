#!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://github.com/rupskygill/ML-mastery/blob/master/deep_learning_with_python_code/28_lstm_larger_gen_text.py

import sqlite3
import numpy as np
import sys

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout, LSTM, Flatten
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import np_utils

model_path = "./data/model.hdf5"
# text_path = "./data/bilibili.txt"
# text_path = "./data/bilibili_small.txt"
text_path = "./data/test.txt"

# def train(text_path, model_path):
raw_text = None
with open(text_path) as f:
    raw_text = f.read().lower()
        # .replace('a', '')\
        # .replace('b', '')\
        # .replace('e', '')\
        # .replace('h', '')\
        # .replace('1', '')\
        # .replace('2', '')\
        # .replace('3', '')\
        # .replace('6', '')\
        # .replace('0', '')\
        # .replace('.', '')\
        # .replace('\n', '')\
        # .replace(' ', '')


chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_chars = len(raw_text)
n_vocab = len(chars)

def ints_to_chars(ints):
    return ''.join(list(map(lambda i:int_to_char[i], ints)))

def print_data(dataX, dataY):
    for i in range(len(dataX)):
        print("X:%s y:%s" % (ints_to_chars(dataX[i]), int_to_char[dataY[i]]))


def print_Xy(X, y):
    for i in range(len(X)):
        x_ = list(map(lambda x:x[0], X[i]))
        y_ = np.where(y[i]==1)[0][0]
        print("X:%s y:%s" % (ints_to_chars(x_), int_to_char[y_]))

# prepare the dataset of input to output pairs encoded as integers
seq_length = 4
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    if i % 100000 == 0: print('Loading dataX: %d/%d' % (i, n_chars))
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
print("Total Vocab: ", n_vocab)

# reshape X to be [samples, time steps, features]
X = np.reshape(dataX, (n_patterns, seq_length, 1))
y = np_utils.to_categorical(dataY)

model = Sequential()
model.add(LSTM(1024*10, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
# model.add(Flatten())
# model.add(LSTM(64))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(X, y, 
    epochs=5,
    batch_size=128,
    callbacks=[
        # EarlyStopping(monitor='loss', min_delta=0, patience=1, verbose=0, mode='auto'),
        # ModelCheckpoint("./data/weights-{epoch:02d}-{loss:.4f}.hdf5", monitor='loss', verbose=1, save_best_only=True, mode='min'),
    ])

model.save(model_path)

# train(text_path, model_path)
# model = load_model(model_path)

start = np.random.randint(0, len(dataX)-1)
pattern = dataX[start]
result = ''
print("输入:\"%s\"" % ''.join([int_to_char[value] for value in pattern]))
# generate characters
for i in range(10):
    x = np.reshape(pattern, (1, len(pattern), 1))
    x = x / float(n_vocab)
    prediction = model.predict(x, verbose=0)
    index = np.argmax(prediction)
    char = int_to_char[index]
    seq_in = [int_to_char[value] for value in pattern]
    # print('pattern:', pattern)
    # print('结果：%s' % (ints_to_chars(pattern)))
    # sys.stdout.write(result)
    pattern.append(index)
    result += char
    pattern = pattern[1:len(pattern)]
print("补完:\"%s\"" % result)

