import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

# Used to quantify how good our predictions are
def mean_square_error(Y_test, Y_pred):
    return round(np.square(np.subtract(Y_test,Y_pred)).mean(), 4) 

# Pathways
DATAFRAME = 'data/final-dataset.csv'

# Load the datasets into pandas dataframes
df = pd.read_csv(DATAFRAME, low_memory=False)

# Get rid of the 'date' column
df = df.drop('date', axis=1)
cols = df.columns.values

# Transform the data to values between a certain range
# An important step for making the gradient descent run a lot more efficiently
x_scaler = MinMaxScaler(feature_range=(0, 1))
x_scaler.fit(df.drop(columns='SA_WS1_POA'))
y_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler.fit(df.SA_WS1_POA.values.reshape(-1, 1))

# Split the data into a test and train set
train, test = train_test_split(df, test_size=0.2)

# Convert them back to Dataframes just to make life a little simpler
x_train = train.drop(columns='SA_WS1_POA')
y_train = train.SA_WS1_POA
x_test  = test.drop(columns='SA_WS1_POA')
y_test  = test.SA_WS1_POA

filename = 'pickles/mlp_regressor5x50.sav'

# Either open up an existing pickled model or start training a new one
# mlp = pickle.load(open(filename, 'rb'))
mlp = MLPRegressor(solver='sgd', activation='relu', alpha=.1, learning_rate='adaptive',
                   hidden_layer_sizes=(100, 100, 100, 100, 100), random_state=1, verbose=True)
mlp.fit(x_scaler.transform(x_train), y_scaler.transform(y_train.values.reshape(-1, 1)).ravel())
pickle.dump(mlp, open(filename, 'wb'))

pred = np.asarray(mlp.predict(x_scaler.transform(x_test)), dtype=np.float32).reshape(-1, 1)
pred = y_scaler.inverse_transform(pred)
pred = np.around(pred, decimals=2)

res = pd.DataFrame({'Prediction': pred.ravel(), 'Actual': y_test.values.ravel()})
print(res)
print()
print("loss = " + str(mean_square_error(pred.ravel(), y_test.ravel())))