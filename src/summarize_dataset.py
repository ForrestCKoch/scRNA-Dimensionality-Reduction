import os
import sys
import pickle
import pandas as pd
import numpy as np
from sc_dr.datasets import FromPickledPanda

if __name__ == '__main__':
    path = sys.argv[1]
    X = FromPickledPanda(path)

    cell_types = sorted(set(X.labels))
    ncells = str(len(X))
    ngenes = str(X.dims)
    perc0 = str(np.sum(X.data==0)/(X.data.size))
    print(','.join([ncells,ngenes,perc0,'"'+', '.join(cell_types)+'"']))

