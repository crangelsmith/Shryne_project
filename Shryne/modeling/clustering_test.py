import pandas as pd
import numpy as np
import sklearn as skl
import scipy as sci
from collections import defaultdict

# load in the Df
df = pd.read_pickle('../data/relationship_features_forclustering.pandas_df')

dd = defaultdict()
for i, contact in enumerate(df['contact_id'].unique()):
    sub_df = df[df['contact_id'] == contact]
    for col in list(sub_df):
        try:
            dd[col].append(sub_df[col].isnull().sum() / float(sub_df[col].size))
        except:
            dd[col] = [sub_df[col].isnull().sum() / float(sub_df[col].size)]

print dd