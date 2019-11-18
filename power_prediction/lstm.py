import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

FILENAME = 'data/final-dataset.csv'
TEST_TRAIN_RATIO = .75

# fix random seed for reproducibility
np.random.seed(7)

# Load the datasets into pandas dataframes
# Change the DateTime to UNIX epoch time (seconds)
# and then mod by 60*60*24 to get time of day in seconds
df = pd.read_csv(FILENAME, low_memory=False)
df['date'] = (pd.to_datetime(df['date']) - datetime(1970,1,1)).astype('timedelta64[s]') % (60*60*24)

# Transform all the data so that the activation function works a lot better
scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(df)
# df = df[:10000, :]
	
# Split into train and test sets
train_size = int(len(df) * TEST_TRAIN_RATIO)
train, test = df[0:train_size, :], df[train_size:-1, :]

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), :]
		dataX.append(a)
		dataY.append(dataset[i + look_back, :])
	return np.array(dataX), np.array(dataY)

look_back = 10
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
# trainX = np.reshape(trainX, (trainX.shape[0], look_back, trainX.shape[1]))
# testX = np.reshape(testX, (testX.shape[0], look_back, testX.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(10, 12)))
model.add(Dense(12))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

# ================= SAVING THE MODEL =================
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
# ================= SAVING THE MODEL =================
 
# # ================= LOADING THE MODEL =================
# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)
# # load weights into new model
# model.load_weights("model.h5")
# print("Loaded model from disk")
# # ================= LOADING THE MODEL =================

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[:, 11], trainPredict[:, 11]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[:, 11], testPredict[:, 11]))
print('Test Score: %.2f RMSE' % (testScore))