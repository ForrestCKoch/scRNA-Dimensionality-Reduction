import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

df = pd.read_csv(sys.argv[1])
dims = pd.read_csv('dims-'+sys.argv[1])
direction = False
fill = 0
if sys.argv[1] == 'db.csv':
    direction = True
    fill = 1
sns.heatmap(df.set_index('dataset').fillna(fill).rank(ascending=direction,axis=1),annot=
    dims.set_index('dataset').fillna(-1))
plt.show()
