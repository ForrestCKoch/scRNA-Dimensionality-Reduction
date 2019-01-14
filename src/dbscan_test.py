
import pickle
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np

from sklearn.cluster import DBSCAN

# #############################################################################
emb_file = 'data/embeddings/' + sys.argv[1] + '-250k-embedding.pickle'
X = pickle.load(open(emb_file,'rb'))

#X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN
#db = DBSCAN(min_samples=100).fit(X)
db = DBSCAN().fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

# #############################################################################
# Plot result
# Black removed and is used for noise instead.
unique_labels = set(labels)
#colors = [plt.cm.Spectral(each)
#          for each in np.linspace(0, 1, len(unique_labels))]
#colors = plt.cm.Spectral(labels)
#colors = cm.get_cmap()(labels)

plt_file = 'data/plots/'+sys.argv[1]+'-250k.pdf'

plt.scatter(X[:,0],X[:,1],c=labels,s=1,marker=',')

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.savefig(plt_file)
