import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import time
import datetime
import json
import helpers

stemmer = LancasterStemmer()

training_data = []
with open('data.json') as json_file:
    training_data = json.load(json_file)['data']

import nltk
from nltk.corpus import stopwords

ignore_words = set(stopwords.words('english'))
words = []
documents = []

for pattern in training_data:
    w = nltk.word_tokenize(pattern['sentence'])
    words.extend(w)
    documents.append((w, pattern['class']))

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

training = []

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)

from sklearn import preprocessing

le = preprocessing.LabelEncoder()
labels = []
for x in training_data:
    labels.append(x['class'])
features = le.fit_transform(labels)

def getAction(query):
    X = np.array(training)
    y = np.array(features)
    test = np.array([helpers.bow(query, words)])

    import nb
    prediction = nb.classify(X, y, test)
    predicted_class = le.inverse_transform(prediction)
    return predicted_class[0]
