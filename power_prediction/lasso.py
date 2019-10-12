import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.preprocessing import MinMaxScaler

# Pathways
TRAIN = 'data/train-data.csv'
TEST  = 'data/test-data.csv'

# Load the datasets into pandas dataframes
train = pd.read_csv(TRAIN, low_memory=False)
test  = pd.read_csv(TEST, low_memory=False)

# Get rid of the 'date' column
train = train.drop('date', axis=1)
test  = test.drop('date', axis=1)

# Convert to numpy arrays
train = train.values
test  = test.values

# Used to quantify how good our predictions are
def mean_square_error(Y_test, Y_pred):
    return round(np.square(np.subtract(Y_test,Y_pred)).mean(), 4) 

# Normalize the data
x_train = np.delete(train, 9, 1)
y_train = train[:, 10].reshape(-1, 1)
x_test  = np.delete(test , 9, 1)
y_test  = test[:, 10]

# Normaloize/Scale all the data
x_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler = MinMaxScaler(feature_range=(0, 1))
x_train = x_scaler.fit_transform(x_train)
y_train = y_scaler.fit_transform(y_train)
x_test  = x_scaler.fit_transform(x_test)

lasso = Lasso()

parameters = {'alpha': np.arange(0.001, .01, 0.0001)}

lasso_regressor = GridSearchCV(lasso, parameters, scoring='neg_mean_squared_error', cv=5)

lasso_regressor.fit(x, y_train)

# print(lasso_regressor.best_params_)
# print(lasso_regressor.best_score_)

pred = np.asarray(lasso_regressor.best_estimator_.predict(x_test), dtype=np.float32)

results = {'Prediction': np.around(pred, decimals=2),
           'Actual': test.pwr_out.values}

res = pd.DataFrame(results)
print(res)
print()
print("MSE: " + str(mean_square_error(res.Prediction.values, res.Actual.values)))
