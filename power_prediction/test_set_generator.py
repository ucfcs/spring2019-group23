# Creates a testing dataset of random elements from the original dataset

import random
import pandas as pd
import numpy as np

TRAIN = 'data/train-data.csv'
TEST  = 'data/test-data.csv'

# Load the dataset
df   = pd.read_csv(TRAIN, low_memory=False)
test = pd.read_csv(TEST,  low_memory=False)

h = set()
while test.shape[0] < 25000:
    r = random.randint(0, df.shape[0])
    print(test.shape[0])
    if r not in h:
        test = test.append(df.iloc[r])
        df = df.drop(df.index[r])
        h.add(r)

df.to_csv(path_or_buf=TRAIN, index=False, sep=',')
test.to_csv(path_or_buf=TEST, index=False, sep=',')