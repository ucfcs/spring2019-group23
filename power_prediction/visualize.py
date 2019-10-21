from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns; sns.set()
import pandas as pd
import numpy as np

# Pathway
DATASET = 'data/test-data.csv'

# Load the dataset
df = pd.read_csv(DATASET, low_memory=False)

# Function to make it easier to display graphs
def scatter_plot(x, y):
    plt.figure(figsize=(16,8))
    plt.scatter(df[x], df[y], s=.5, color='navy')
    plt.xlabel('Wind Direction (Degrees)')
    plt.ylabel('Power Output (kW)')
    plt.show()

def scatter_plot_3d(x, y, z):
    fig = plt.figure(figsize=(16,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df[x], df[y], df[z], s=.5, color='navy')
    plt.xlabel(x)
    plt.ylabel(y)
    # plt.zlabel(z)
    plt.show()

# scatter_plot_3d('PSP1_Irrad_Avg', 'Ambient_RH1_Avg', 'SA_WS1_POA')
# scatter_plot('Ambient_RH1_Avg', 'SA_WS1_POA')

print(np.mean(df.SA_WS1_POA.values)) 