import pickle
from collections import Counter

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Activation, LeakyReLU
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
import pandas as pd
import coord_to_suburb
import keras.backend as k

model = Sequential()
model.add(Dense(32, input_shape=(19,)))
model.add(Activation("tanh"))
model.add(Dense(64))
model.add(Activation("tanh"))
model.add(Dropout(0.2))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile(loss='mean_squared_error', optimizer='adam')


def get_x_and_y():
    file = open("data/prepared_data.pkl", "rb")
    pkl = pickle.load(file)
    # file2 = open("data/coordinates.pkl", "rb")
    # pkl2 = pickle.load(file2)
    X = []
    y = []
    files = ["employment"]

    for i in pd.read_csv("data/employment_sub.csv").values:
        y.append(100 - i[15])

    # pkl2 = coord_to_suburb.locations_to_suburb_count(pkl2)
    #
    # pkl = [pkl[i].update(pkl2[i]) for i in range(len(pkl))]
    for i in range(len(pkl)):
        temp = [0 if val is None else val for val in list(pkl[i].values())]
        if sum(temp) and y[i]:
            X.append(np.array(temp))
        else:
            y[i] = False

    y = [i for i in y if i]
    print(Counter(y))
    X = np.array(X)
    y = np.array(y)
    return train_test_split(X, y)


file = open("data/prepared_data.pkl", "rb")
pkl = pickle.load(file)
features = list(pkl[0].keys())

save = open("X.pkl", "wb")


X_train, X_test, y_train, y_test = get_x_and_y()

data_file = open("data/all_data.pkl", "wb+")
pickle.dump([X_train, X_test, y_train, y_test], data_file)


model.fit(x=X_train, y=y_train, epochs=200, validation_split=0.2, verbose=1, batch_size=128)

print(model.predict(X_test))
print(np.average(np.abs(y_test - model.predict(X_test))))


def suggest_improvements(Xs):
    sess = k.get_session()
    sess.run(tf.global_variables_initializer())
    return sess.run(tf.gradients(model.output, model.input), feed_dict={model.input: Xs})


index = coord_to_suburb.get_suburb_list().index("Berwick")

gradients = suggest_improvements([X_test[index]])[0][0]

improvements = {features[i]: (gradients[i]) for i in range(len(gradients))}

print(improvements)
