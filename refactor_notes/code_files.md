# Step 00 -- Data Prep
* : 00-00_install-r-packages.R : r_packages.R
    * attempt to install prerequisite R packages ...
* convert_csv_to_pd.py
    * input: **dataset name** as `ds`
    * converts `*.csv.gz` files to pickled pandas.DataFrame 
* convert_datasets.sh
    * calls `scripts/convert_sce_to_csv.R` and `scripts/convert_csv_to_pd.py` for each dataset from `data/datasets/rds`
* convert_sce_to_csv.R
    * for each `*.rds` in `data/datasets/rds`, convert the SingleCellExperiment data structure into csv format -- two files are produced:
    for log-transformed and non-transformed counts.
* download_sce_datasts.sh
    * clones into my forked repo for `scRNA.seq.datasets`, and uses the relevent bash/Rscripts to create RDS files
    * **note:** there may be some bugs in this step -- consider rerunning to make sure it is smooth

# Step 01 -- Embedding Calculation
* generate_all_embeddings.sh
    * bash script wrapper which uses qsub to submit `run_generate_embedding.sh` for each required embedding
* generate_gpu_embeddings.sh
    * bash script wrapper to sequentially generate embeddings for the two gpu methods (vasc and ???)
* restart_failed.sh
    * helper script to restart failed calculations of embeddings    
* run_generate_embedding.sh
    * bash script wrapper round src/generate_embedding.py intended to be used for qsub 

# Step 02 -- IVM Calculation

# Step 03 -- Calculate Preservation of Global Structure
* measure_pairwise_distances2.py
* measure_pairwise_distances3.py
* measure_pairwise_distances.py
    * **note:** further work needed
    * not sure what the difference between these three files is, but caclculates the correlation of pairwise distances before and after DR
* parallel_pairwise_args.txt
    * used in combination with xargs and parallel_pairwise.sh to compute measure_pairwise_distances.py in parallel
* parallel_pairwise.sh
    * see above
* setup_pool.sh
    * sets up file-system based queue to run each of the DBSCAN optimization jobs

# Step 04 -- DBSCAN optimization preprocessing
* generate_queues.sh
    * calls generate_trials.py for each of the distiance measures to create a queue of trials for DBSCAN
    * suggested usage is `cat data/results/eps_upperbounds.csv | head -n+2 | xargs -n1 -P 8 -I {} bash scripts/generate_queues.sh {}`
    * **requires** epsilon upperbounds to have been calculated -- input format is rather particular to the output of `get_eps_bounds.py`
* generate_trials.py
    * randomly samples according to provided parameters to provide hyperparameters for DBSCAN optimization
* get_eps_bounds.py
    * calculate pairwise distances in order to determine the minimum value of epsilon such that DBSCAN will result in at least one cluster

# Step 05 -- DBSCAN cluster calculation
* run_trial.sh
    * bash script wrapper around src/run_dbscan_trials.py 
* self_submitting.sh
    * self submitting script for Raijin to repetedly call cluster-pool.sh

# Step 06 -- IVM Analyses
* ivm_analysis.R
    * calculate Kendall's W: between IVMs, between distance measures, and between datasets.
* ivm_concordance_analysis-medians.R
    * same as `ivm_analysis.R`, but uses medians in place of means
* ivm_correlation_with_pw_cor.R
    * calculate spearman correlations between IVMs and preservation of global structure ... consider removing as I don't believe this is a valid anlysis
* ivm_mean_rank_analysis.R
    * **remove?**
    * calculates mean rank of methods in each dataset
* ivm_rank_analysis-2.R
    * **empty**
* ivm_sign_test_pval_heatmaps_combined.py
    * creates Figure 3 displaying heatmaps of p-values comaparing methods within an IVM
* ivm_sign_test_pval_heatmaps.py
    * creates individual heatmaps from figure 3
* ivm_sign_test.R
    * calculate Sign test results between methods for each IVM
* plot_internal_results_heatmap.py
    * input: `data/reults/internal_validation_measures/internal_measures_reduced.csv`
    * cretaes the heatmap for Figure 2

# Step 07 -- Global Structure Analyses
* combine_ivm_correlation_data.py
    * input: `data/results/internal_validation_measures/internal_measures_reduced.csv`, `data/results/pairwise_distances/pairwise_correlations_all.csv`
    * output: `data/results/pw_correlations/best_ivm_combined_pw_cor.csv`
* pairwise_correlation_boxplots.R
    * create boxplots showing the correlation of pairwise distances across datasets for each method
* plot_pairwise_distance_correlations.py
    * creates `data/results/pw_correlations/pw_correlations_by_best_ivm.csv`
    * created `writeup/plots/pw_correlations.pdf`, but this is now commented out

# Step 08 -- DBSCAN results analysis
* dbscan_analysis.R
    * prints the mean ARI of each method's performance on DBSCAN optimization for each of the distance metric/ivm combinations
    * **note:** this should probably be refactored to output a csv 
* dbscan_barplots.R
    * output barplots of correlation of ARI from DBSCAN optimization with dataset properties `n_classes`, `n_samples`, `min_class_perc`,
    `max_class_perc`, `protocol`.
* dbscan_ivm-dist_comparison.R
    * calculate pairwise Sign and Wilcoxon Sign Rank tests to compare within DRM differences in ARI from different distance metric/IVM pairings.
    * **note:** this should probably be refactored to output a csv 
* dbscan_median_analysis.R
    * prints the median ARI across datasets for each method -- one row for each pair of distance metric and IVM.
    * should be used in Table 4 to replace Averages ...
    * **note:** this should probably be refactored to output a csv 
* dbscan_seu-vrc_pairwise_heatmaps.py
    * intputs: `writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods.csv`,`writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods_filtered.csv`,
    `writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods.csv`, `writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods_filtered.csv` 
    * **note:** check which script produce these csvs -- probably dbscan_seu-vrc_pairwise_tests.R
    * used in Figure 6
* dbscan_seu-vrc_pairwise_tests.R
    * Calculate pairwise Sign and Wilcoxon Sign Rank tests to compare between DRM differences in ARI when using SEU-VRC optimized clusterings.
* dbscan_vs_ivm_analysis.R
    * plots mean/meadian rank of DRM in the IVM analysis vs DBSCAN analysis -- also calculate 
* get_best_dbscan_trial_cor.py
    * find the "best" dbscan clusterings when using correlation distance measure
* get_best_dbscan_trial_cos.py
    * find the "best" dbscan clusterings when using cosine distance measure
* get_best_dbscan_trial_parallel_highdim.py
    * find the "best" dbscan clusterings in parallel (using multiple cores), but ignore embeddings with fewer than 16 dimension
* get_best_dbscan_trial_parallel.py
    * find the "best" dbscan clusterings in parallel (using multiple cores)
* get_best_dbscan_trial.py
    * find the "best" dbscan clusterings when using euclidean distance measure
* get_best_dbscan_trial_sec.py
    * find the "best" dbscan clusterings when using seuclidean distance measure
* pairwise_sign_test_dbscan.R
    * calculate pairwise sign tests between ??? for DBSCAN results
* plot_dbscan_results_heatmap.py
    * input: metric, acc, opt
    * creates heatmap with boxplots of the style for Figure 5
* plot_dbscan_results_heatmap_old.py

# Step 09 -- Resource Analysis
* get_resource_results.sh
    * parse through the log files to get time and memory information for each embedding
* plot_resources.R
    * create some plots for memory/time usage

# MISC
* aggregate_concordance.R
    * **empty file** 
* plot_2d_embedding.py
    * helper script to generate a 2d plot from a specified embedding (call python3 scripts/plot_2d_embedding.py filename [d1 d2])
* plot_best_dbscan_trial.py
    * plot 2d scatterplots of select methods/datasets which had good dbscan performance
* plot_best_ivm.py
    * plot 2d scatterplots of select methods/datasets which had good ivm performance
* get_best_kmean_trial_parallel.py
    * find the "best" kmeans clusterings in parallel (using multiple cores)
* plot_kmean_results_heatmap.py
    * same as dbscan equivalent but for kmean results ...
* pwd_analysis.R
    * calculate pairwise wilcoxon rank sign tests between different IVMs for preservation of global structure -- probably not useful/valid
* run_all.sh
    * **remove** currently just downloads and converts datasets ...
* sivm_dinfo_reshape.sh
    * **???**

src/
src/run_kmeans_trials.py
src/generate_embedding.py
src/get_internal_validation_measures.py
src/run_dbscan_trials.py
src/summarize_dataset.py
src/sc_dr
src/sc_dr/sumarize.py
src/sc_dr/clustering.py
src/sc_dr/metrics.py
src/sc_dr/__init__.py
src/sc_dr/datasets.py
