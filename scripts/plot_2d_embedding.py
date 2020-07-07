import sys
import pickle as pkl
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder as le

if __name__ == '__main__':
    with open(sys.argv[1],'rb') as fh:
        x = pkl.load(fh)
    colors = le().fit_transform(x.cell_type)
    plt.scatter(x[0],x[1],c=colors,s=0.5)
    plt.show()

