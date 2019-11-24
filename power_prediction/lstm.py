import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

TEST_TRAIN_RATIO  = .75
LOOK_BACK         = 90
PREDICTION        = 15
FILENAME          = 'data/final-dataset.csv'
MODEL_JSON_NAME   = 'models/lstm_' + str(PREDICTION) + 'p_' + str(LOOK_BACK) + '_l_pvp.json'
MODEL_WEIGHT_NAME = 'weights/lstm_' + str(PREDICTION) + 'p_' + str(LOOK_BACK) + '_l_pvp.h5'

# fix random seed for reproducibility
np.random.seed(0)

# Load the datasets into pandas dataframes
df = pd.read_csv(FILENAME, low_memory=False)

# Extract the hour from the datetime. Hour is probably the unit of time with the most info.
# There's a difference in sunlight between 5:00 and 6:00, but 5:00 and 5:01 are very similar.
df['date'] = pd.to_datetime(df['date']).dt.hour

# Transform all the data so that the activation function works a lot better
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_df = scaler.fit_transform(df)

# Split into train and test sets
train_size = int(len(scaled_df) * TEST_TRAIN_RATIO)
train, test = scaled_df[0:train_size, :], scaled_df[train_size:-1, :]

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(look_back, len(dataset) - PREDICTION):
		a = dataset[i-look_back:i,:]
		dataX.append(a)
		dataY.append(dataset[i + PREDICTION - 1,:])
	return np.array(dataX), np.array(dataY)

trainX, trainY = create_dataset(train, LOOK_BACK)
testX, testY = create_dataset(test, LOOK_BACK)

# You never want both the 'TRAINING' and 'LOADING' blocks of code uncommented at the same time.
# Make sure that when one is uncommented. The other is commented out.
# ================== TRAINING & SAVING THE MODEL ==================
# Create and fit the LSTM network
model = Sequential()
model.add(LSTM(40, activation='relu', return_sequences=True, input_shape=(LOOK_BACK, scaled_df.shape[1])))
model.add(Dropout(0.2))
model.add(LSTM(40, activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(40, activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(40, activation='relu'))
model.add(Dense(scaled_df.shape[1]))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=5, batch_size=32, verbose=2)

# Serialize model to JSON
model_json = model.to_json()
with open(MODEL_JSON_NAME, 'w') as json_file:
    json_file.write(model_json)

# Serialize weights to HDF5
model.save_weights(MODEL_WEIGHT_NAME)
print("Saved model to disk")
# ================== TRAINING & SAVING THE MODEL ==================

# # ======================= LOADING THE MODEL =======================
# # load json and create model
# json_file = open(MODEL_JSON_NAME, 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)
# # load weights into new model
# model.load_weights(MODEL_WEIGHT_NAME)
# print("Loaded model from disk")
# # ======================= LOADING THE MODEL =======================

# Make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# Invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)

# Calculate root mean squared error and print results
results = pd.DataFrame({'Prediction': testPredict[:,11], 'Actual': testY[:,11]})
print(results.sample(frac=1))
trainScore = math.sqrt(mean_squared_error(trainY[:,11], trainPredict[:,11]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[:,11], testPredict[:,11]))
print('Test Score: %.2f RMSE' % (testScore))

# Visualize the predictions and ground truth
def create_scatter_graph(x, y, c, title):
	plt.figure()
	plt.scatter(x=x, y=y, s=.5, c=c)
	plt.title(title)
	plt.xlabel('Irradiance ($kW/m^{2}$)')
	plt.ylabel('Photovoltaic Power Output ($kW$)')
	plt.tight_layout()

df = df.values
create_scatter_graph(testY[:,3], testPredict[:,11], 'b', "Model's Prediction")
create_scatter_graph(testY[:,3], testY[:,11], 'r', "Ground Truth")
plt.show()