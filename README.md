# SVR2019-DL-Models
Repository for the deep learning models I used in my 2019 summer vacation research at UNSW

## Usage
### e18MouseData.py
`e18MouseData.py` provides a Dataset class `E18MouseData` which can be used create a PyTorch friendly Dataset from GSE93421_bbrain_aggregate_matrix.hdf5. 

## Data
This code is intended to be used with GSE93421_brain_aggregate_matrix.hdf5 (ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE93nnn/GSE93421/suppl/GSE93421_brain_aggregate_matrix.hdf5).  Further information is available [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE93421); however, I have been unable to find a thorough description detailing how this dataset is organized.
### Dataset Structure
The following sections represent my best guess at the dataset's structure. The hdf5 file contains 7 1D lists under the head node 'mm10'. 
#### barcodes (n ~= 1.3 million)
Barcode identifier for each sequenced cell
#### data (n ~= 2.6 billion)
Count data.  Each entry corresponds to a reading for a specific gene and cell.  See below for details ...
#### genes and gene_names (n = 27998)
Gene identifiers.
#### indicies (n ~= 2.6 billion)
This list has a 1-1 correspondence with data. Each entry represents an index in `genes`/`gene_names` (0 <= v < 27998).  It indicates what gene the corresponding entry in `data` is refering to.
#### indptr (n ~= 1.3 million)
This is has a 1-1 correspondence with `barcodes`.  Each entry ris a pointer to an index in `data` (monotonically increasing with 0 <= v <~ 2.6 billion).  Each entry in `data` between two consective values of `indptr` are count data for the same cell with the corresponding gene given by `indices`.

## Notes on Computational Resources
This dataset is very large, especially in it's full sparse representation (~36 billion datapoints).  This code will require approximately 170GB of RAM to load the full dataset (I provide the option to only load a fraction of it in).  It takes about 15 minutes to load even using 20 processes in parallel on a dual socket Intel E5-2699 (2.2GHz).

## Dependencies
- [My fork of pt-sdae](https://github.com/ForrestCKoch/pt-sdae) (including a branch compatibale with PyTorch 0.35 for Cuda 7.5)
- [h5py](https://pypi.org/project/h5py/) (for loading in data)
- [sharedmem](https://pypi.org/project/sharedmem/) (to allow large shared-memory numpy arrays between processes)

## Supplementary documents
- [Clustering algorithm summaries -- Google Docs](https://docs.google.com/document/d/1mtiFeIoSJ_2lGqbVKKj2sYF2W-ETbNaZYS48rz337kk/edit?usp=sharing)
- [Other datasets -- Google Docs](https://docs.google.com/document/d/1Qq0xmSaUImlripmNJAZbTILBmiNIg5ApWcTIjz6eN18/edit?usp=sharing)
