from sklearn.cluster import KMeans
import pandas as pd
from scipy.cluster.vq import kmeans
from scipy.spatial.distance import cdist,pdist
from sklearn.decomposition import RandomizedPCA
import numpy as np
import scipy.stats as stats


df = pd.read_pickle('../data/relationship_features_forclustering.pandas_df')
print df.columns()
df_new = df[['message_count', 'word_count','compound','response_time','message_count_reciprocity']]

df_new.dropna(inplace = True)




pca = RandomizedPCA(n_components=2).fit(df_new) # pca is an instance of class randomizedPCA with data['data']

X = pca.transform(df_new) # reduces data from (1797,64) to (1797,2) though not sure how.

print(stats.describe(X))

pred = []
k_means = KMeans(n_clusters = 2, init='k-means++')
pred = k_means.fit_predict(X)
inertia = k_means.inertia_
cluster_centers = k_means.cluster_centers_

df_new["prediction"] =pred

print(pred.sum())
print(len(pred))
print(inertia)
# print(cluster_centers)





