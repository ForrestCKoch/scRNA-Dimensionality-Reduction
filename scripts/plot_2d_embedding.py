import sys
import pickle as pkl
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder as le

if __name__ == '__main__':
    with open(sys.argv[1],'rb') as fh:
        x = pkl.load(fh)
    if(len(sys.argv) == 4):
        d1 = int(sys.argv[2])
        d2 = int(sys.argv[3])
    else:
        d1=0
        d2=1
    colors = le().fit_transform(x.cell_type)
    plt.scatter(x[d1],x[d2],c=colors,s=0.5)
    plt.show()

