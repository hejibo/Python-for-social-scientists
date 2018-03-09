# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
import string
import numpy as nm
import codecs
import re
import collections
import math
import tensorflow as tf
import random
import glob

allWords = []
allDocuments = []
allLabels = []

def readFile(fileName, allWords):


    file = codecs.open(fileName, encoding='utf-8')

    for line in file:
        line = line.lower().encode('utf-8')
        words = line.split()
        for word in words:
            word = word.translate(None, string.punctuation)
            if word != '':
                allWords.append(word)

    file.close()


def readFileToConvertWordsToIntegers(dictionary, fileName, allDocuments, allLabels, label):

    file = codecs.open(fileName, encoding='utf-8')
    document = []
    for line in file:
        line = line.lower().encode('utf-8')
        words = line.split()
        for word in words:
            word = word.translate(None, string.punctuation)
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK'] 
            document.append(index)
        allDocuments.append(document)
        allLabels.append(label)

    file.close()


vocabulary_size = 10000

def build_dataset(words):
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  unk_count = 0
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    else:
      index = 0  # dictionary['UNK']
      unk_count = unk_count + 1
    data.append(index)
  count[0][1] = unk_count
  reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys())) 
  return dictionary, reverse_dictionary


BaseFolder = "/Users/b392t356/Desktop/Python-for-social-scientists/Python - machine learning/sentiment-analysis-master/"
fileList = glob.glob(BaseFolder+"train/neg/*.txt")
for file in fileList:
    readFile(file, allWords)

fileList = glob.glob(BaseFolder+"train/pos/*.txt")
for file in fileList:
    readFile(file, allWords)

print(len(allWords))

dictionary, reverse_dictionary = build_dataset(allWords)
del allWords  # Hint to reduce memory.

print(len(dictionary))

fileList = glob.glob(BaseFolder+"train/neg/*.txt")
for file in fileList:
    readFileToConvertWordsToIntegers(dictionary, file, allDocuments, allLabels, 0)

fileList = glob.glob(BaseFolder+"train/pos/*.txt")
#print("fileList:",fileList)
for file in fileList:
    readFileToConvertWordsToIntegers(dictionary, file, allDocuments, allLabels, 1)

print(len(allDocuments))
print(len(allLabels))

c = list(zip(allDocuments, allLabels)) # shuffle them partitioning

random.shuffle(c)

allDocuments, allLabels = zip(*c)
print('a')

trainX = allDocuments[:25]
testX = allDocuments[25:]

trainY = allLabels[:25]
testY = allLabels[25:]


#counter=collections.Counter(trainY)
#print(counter)





trainX = pad_sequences(trainX, maxlen=100, value=0.)
testX = pad_sequences(testX, maxlen=100, value=0.)
# Converting labels to binary vectors
trainY = to_categorical(trainY, nb_classes=2)
testY = to_categorical(testY, nb_classes=2)

# Network building
net = tflearn.input_data([None, 100])
net = tflearn.embedding(net, input_dim=vocabulary_size, output_dim=128)
net = tflearn.lstm(net, 128, dropout=0.8)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy')

# Training
model = tflearn.DNN(net, tensorboard_verbose=0)
model.fit(trainX, trainY,n_epoch=100, validation_set=(testX, testY), show_metric=True,
          batch_size=32)
predictions = model.predict(trainX)
print(predictions)