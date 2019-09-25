from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import pickle
import seaborn as sns; sns.set()
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

# Pathways
OUC = 'data/power-irradiance.csv'
TRAIN = 'data/final-orlando-report-train.csv'
TEST  = 'data/final-orlando-report-test.csv'

# Load the dataset
df = pd.read_csv(TRAIN)
test = pd.read_csv(TEST)

# Function to make it easier to display graphs
def scatter_plot(x, y):
    plt.figure(figsize=(16,8))
    plt.scatter(df[x], df[y], s=.5)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def scatter_plot_3d(x, y, z):
    fig = plt.figure(figsize=(16,8))
    ax = fig.add_subplot(111, projection='3d')
    plt.scatter(df[x], df[y], df[z], s=.5)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

# scatter_plot('irdnc', 'pwr_out')

# Used to quantify how good our predictions are
def mean_square_error(Y_true, Y_pred):
    return round(np.square(np.subtract(Y_true,Y_pred)).mean(), 4) 

# Normalize the data
scaler = MinMaxScaler(feature_range=(-1, 1))
norm_df = scaler.fit_transform(df)
norm_test = scaler.fit_transform(test)
x = np.delete(norm_df, 0, 1)
x_test = np.delete(norm_test, 0, 1)
y = norm_df[:, 0]
y_true = norm_test[:, 0]

# If Using pandas, this data is not normalized
# x = df.drop(['pwr_out'], axis=1).values
# x_test = test.drop(['pwr_out'], axis=1).values
# y = df['pwr_out'].values
# y_true = test['pwr_out'].values

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

################### MLPRegressor PREDICTION ##################
filename = 'mlp_regressor.sav'

mlp = MLPRegressor(solver='lbfgs', activation='tanh', alpha=1, hidden_layer_sizes=(100, 100, 100, 100), random_state=1, verbose=True)
mlp.fit(x, y)
# mlp = pickle.load(open(filename, 'rb'))

pred = np.asarray(np.around(mlp.predict(x_test), 6), dtype=np.float32)
# pred[pred >  1] = 1
# pred[pred < -1] = -1

results = {'Prediction': pred,
           'Actual': y_true}

res = pd.DataFrame(results)
print(res)
print()
print("loss = " + str(mean_square_error(y_true, pred)))

pickle.dump(mlp, open(filename, 'wb'))
################### MLPRegressor PREDICTION ##################
