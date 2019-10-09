#for dataset in baron-human campbell chen macosko shekhar marques; do 
for dataset in marques; do 
#for dataset in mctsne; do 
    for method in fa fica isomap lda lle mctsne nmf pca sdae umap; do
#    for method in fa fica lda mctsne pca sdae umap pca-scaled; do
        qsub -N run.sh -o logs/dbscan_optimization/logT-${dataset}_${method}.log -e logs/dbscan_optimization/logT-${dataset}_${method}.err -v dataset=${dataset},method=${method} scripts/rocks_dbscan_optimization.sh
    done 
done
