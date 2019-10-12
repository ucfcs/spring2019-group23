from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns; sns.set()

# Pathway
DATASET = 'data/final-dataset.csv'

# Load the dataset
df = pd.read_csv(DATASET, low_memory=False)

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

scatter_plot('irdnc', 'pwr_out')