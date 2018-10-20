from controlers.clustering import *
from controlers.df_manipulations import *
from controlers.distances import *

# read the data
df = pd.read_data('')
members = df['id'].unique()

all_graphs_all_care = make_graphs(df, members)

# calculate the dm matrix
dm, for_which_mem = calculate_distance_matrix(all_graphs_all_care, members)

clusters = spectral_clustering(dm, 5, 'rbf', 0.001)

clusters_df = pd.DataFrame()
clusters_df['Cluster_label'] = clusters
count_clus = calculate_df(clusters_df, 'count', 'Cluster_label')
print(count_clus)
