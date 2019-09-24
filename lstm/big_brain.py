# from keras.models import Sequential
# from keras.layers import Dense
import pandas as pd

from sklearn.datasets import make_regression
from matplotlib import pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.neural_network import MLPRegressor

TRAIN = 'data/final-orlando-report-train.csv'
TEST  = 'data/final-orlando-report-test.csv'

# Load the dataset
df = pd.read_csv(TRAIN)
test = pd.read_csv(TEST)

# Function to make it easier to display graphs
def scatter_plot(feature, target):
    plt.figure(figsize=(16,8))
    plt.scatter(df[feature], df[target], c='black', s=.5)
    plt.ylabel("Power Output (MW)")
    plt.xlabel("Irradiance")
    plt.show()

# Function to calculate the MSE
def mean_square_error(Y_true, Y_pred):
    return np.square(np.subtract(Y_true,Y_pred)).mean() 

x = df.drop(['pwr_out'], axis=1).values
x_test = test.drop(['pwr_out'], axis=1).values
y = df['pwr_out'].values
y_true = test['pwr_out'].values

# Normalize the data from -1 to 1

###################### LASSO PREDICTION ######################
# lasso = Lasso()

# parameters = {'alpha': np.arange(0.001, .01, 0.0001)}

# lasso_regressor = GridSearchCV(lasso, parameters, scoring='neg_mean_squared_error', cv=5)

# lasso_regressor.fit(x, y)

# # print(lasso_regressor.best_params_)
# # print(lasso_regressor.best_score_)

# pred = np.asarray(lasso_regressor.best_estimator_.predict(x_test), dtype=np.float32)

# results = {'Prediction': np.around(pred, decimals=2),
#            'Actual': test.pwr_out.values}

# res = pd.DataFrame(results)
# print(res)
# print()
# print("MSE: " + str(mean_square_error(res.Prediction.values, res.Actual.values)))
###################### LASSO PREDICTION ######################

###################### MLPRegressor PREDICTION ######################
mlp = MLPRegressor(solver='lbfgs', alpha=1, hidden_layer_sizes=(1000,), random_state=1)
mlp.fit(x, y)

pred = np.asarray(np.around(mlp.predict(x_test), 2), dtype=np.float32)

results = {'Prediction': pred,
           'Actual': y_true}

res = pd.DataFrame(results)
print(res)
print()
print("MSE: " + str(mean_square_error(y_true, pred)))
###################### MLPRegressor PREDICTION ######################
