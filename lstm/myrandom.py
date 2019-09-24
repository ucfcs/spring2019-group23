import random
import pandas as pd

TRAIN = 'data/final-orlando-report-train.csv'
TEST  = 'data/final-orlando-report-test.csv'

# Load the dataset
df   = pd.read_csv(TRAIN)
test = pd.read_csv(TEST)

list = []
while test.shape[0] < 1000:
    r = random.randint(0, df.shape[0])
    print(test.shape[0])
    if r not in list:
        test = test.append(df.loc[r])
        df   = df.drop(r)
        list.append(r)

df.to_csv(path_or_buf='data/final-orlando-report-train.csv', index=False, sep=',')
test.to_csv(path_or_buf='data/final-orlando-report-test.csv', index=False, sep=',')
