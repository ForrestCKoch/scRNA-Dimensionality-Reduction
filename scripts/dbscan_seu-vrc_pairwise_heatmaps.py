import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 8})

wilcox_full = pd.read_csv('writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods.csv')
wilcox_filtered = pd.read_csv('writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods_filtered.csv')
sign_full = pd.read_csv('writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods.csv')
sign_filtered = pd.read_csv('writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods_filtered.csv')

wilcox_full.set_index('Unnamed: 0',inplace=True)
wilcox_filtered.set_index('Unnamed: 0',inplace=True)
sign_full.set_index('Unnamed: 0',inplace=True)
sign_filtered.set_index('Unnamed: 0',inplace=True)

fig, axes = plt.subplots(2,2,figsize=(8,8))
sns.heatmap(wilcox_full,cmap='viridis',vmax=0.7,xticklabels=list(wilcox_full.index),
        yticklabels=list(wilcox_full.index), ax=axes[0][0])
axes[0][0].set_title('Wilcox All Datasets')
axes[0][0].set_ylabel('')

sns.heatmap(wilcox_filtered,cmap='viridis',vmax=0.7,xticklabels=list(wilcox_filtered.index),
        yticklabels=list(wilcox_filtered.index),ax=axes[0][1])
axes[0][1].set_title('Wilcox -- Datasets with max ARI > 0.5')
axes[0][1].set_ylabel('')

sns.heatmap(sign_full,cmap='viridis',vmax=0.7,xticklabels=list(sign_full.index),
        yticklabels=list(sign_full.index),ax=axes[1][0])
axes[1][0].set_title('Sign-test All Datasets')
axes[1][0].set_ylabel('')

sns.heatmap(sign_filtered,cmap='viridis',vmax=0.7,xticklabels=list(sign_filtered.index),
        yticklabels=list(sign_filtered.index),ax=axes[1][1])
axes[1][1].set_title('Sign-test -- Datasets with max ARI > 0.5')
axes[1][1].set_ylabel('')

plt.tight_layout()
#plt.show()
plt.savefig('writeup/plots/dbscan_vrc-seu_pw-test_heatmap.pdf')
