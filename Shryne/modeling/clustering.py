from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_pickle('../data/relationship_features_forclustering.pandas_df')

df.dropna(inplace = True)

df_new = df[['message_count', 'word_count','compound','response_time']]


pred = []
k_means = KMeans(n_clusters = 2, init='k-means++')
pred = k_means.fit_predict(df_new)
inertia = k_means.inertia_
cluster_centers = k_means.cluster_centers_

print(pred.sum())
print(len(pred))
print(inertia)
print(cluster_centers)





