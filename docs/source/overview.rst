Benchmark Overview
==================

Step 00 -- Data Prep
--------------------
- 00-00_install-r-packages.R
    - attempt to install prerequisite R packages ...
- 00-01_download_sce_datasets.sh
    - clones into my forked repo for `scRNA.seq.datasets`, and uses the relevent bash/Rscripts to create RDS files
    * **note:** there may be some bugs in this step -- consider rerunning to make sure it is smooth
- 00-02_convert_sce_to_csv.R
    - for each `*.rds` in `data/datasets/rds`, convert the SingleCellExperiment data structure into csv format -- two files are produced:
    for log-transformed and non-transformed counts.
- 00-03_convert_csv_to_pd.py
    - input: **dataset name** as `ds`
    - converts `*.csv.gz` files to pickled pandas.DataFrame 

Step 01 -- Embedding Calculation
--------------------------------
- src/generate_embedding.py
- 01-00-main_generate_all_embeddings.sh 
    - bash script wrapper which uses qsub to submit `run_generate_embedding.sh` for each required embedding

- 01-01-main_generate_gpu_embeddings.sh 
    - bash script wrapper to sequentially generate embeddings for the two gpu methods (vasc and ???)

Step 02 -- IVM Calculation
--------------------------
- src/get_internal_validation_measures.py

Step 03 -- Calculate Preservation of Global Structure
-------------------------------------------------------
- 03-00-main_parallel_pairwise.sh 
    - see below
- 03-00-a_measure_pairwise_distances.py 
    - **note:** further work needed
    - not sure what the difference between these three files is, but caclculates the correlation of pairwise distances before and after DR
    - **move to subfolder?**
- parallel_pairwise_args.txt
    - used in combination with xargs and parallel_pairwise.sh to compute measure_pairwise_distances.py in parallel
    - **move to subfolder?**

Step 04 -- DBSCAN optimization preprocessing
---------------------------------------------
- 04-00_get_eps_bounds.py 
    - calculate pairwise distances in order to determine the minimum value of epsilon such that DBSCAN will result in at least one cluster
- 04-01-main_generate_queues.sh 
    - calls generate_trials.py for each of the distiance measures to create a queue of trials for DBSCAN
    - suggested usage is `cat data/results/eps_upperbounds.csv | head -n+2 | xargs -n1 -P 8 -I {} bash scripts/generate_queues.sh {}`
    - **requires** epsilon upperbounds to have been calculated -- input format is rather particular to the output of `get_eps_bounds.py`
- 04-01-a_generate_trials.py 
    - randomly samples according to provided parameters to provide hyperparameters for DBSCAN optimization
- 04-02_setup_pool.sh 
    - sets up file-system based queue to run each of the DBSCAN optimization jobs
    - **need to include cluster_pool.sh**

Step 05 -- DBSCAN cluster calculation
-------------------------------------
- src/run_dbscan_trials.py
- 05-00-main_run_trial.sh 
    - bash script wrapper around src/run_dbscan_trials.py 
- 05-00-sge_self_submitting.sh 
    - self submitting script for Raijin to repetedly call cluster-pool.sh

Step 06 -- IVM Analyses
-----------------------
- 06-00_plot_internal_results_heatmap.py 
    - input: `data/reults/internal_validation_measures/internal_measures_reduced.csv`
    - creates the heatmap for Figure 2
- 06-01_ivm_concordance_analysis.R ivm_concordance_analysis-medians.R
    - same as `ivm_analysis.R`, but uses medians in place of means
- 06-02_ivm_sign_tests.R 
    - calculate Sign test results between methods for each IVM
- 06-03_ivm_sign_test_heatmap.py 
    - creates Figure 3 displaying heatmaps of p-values comaparing methods within an IVM

Step 07 -- Global Structure Analyses
------------------------------------
- 07-00_combine_ivm_correlation_data.py 
    - input: `data/results/internal_validation_measures/internal_measures_reduced.csv`, `data/results/pairwise_distances/pairwise_correlations_all.csv`
    - output: `data/results/pw_correlations/best_ivm_combined_pw_cor.csv`
- 07-01_correlation_with_pw_cor.R 
    - calculate spearman correlations between IVMs and preservation of global structure ... consider removing as I don't believe this is a valid anlysis
- 07-02_pairwise_correlation_boxplots.R 
    - create boxplots showing the correlation of pairwise distances across datasets for each method
- 07-03_plot_pairwise_distance_correlations.py 
    - creates `data/results/pw_correlations/pw_correlations_by_best_ivm.csv`
    - created `writeup/plots/pw_correlations.pdf`, but this is now commented out

Step 08 -- DBSCAN results analysis
----------------------------------
- 08-00_get_best_dbscan_trial_parallel.py 
    - find the "best" dbscan clusterings in parallel (using multiple cores)
- 08-01_plot_dbscan_results_heatmap.py 
    - input: metric, acc, opt
    - creates heatmap with boxplots of the style for Figure 5
- 08-03_dbscan_median_analysis.R 
    - prints the median ARI across datasets for each method -- one row for each pair of distance metric and IVM.
    - should be used in Table 4 to replace Averages ...
    - **note:** this should probably be refactored to output a csv 
- 08-03_alt_dbscan_mean_analysis.R 
    - prints the mean ARI of each method's performance on DBSCAN optimization for each of the distance metric/ivm combinations
    - **note:** this should probably be refactored to output a csv 
- 08-04_dbscan_ivm-and-distance-metric_comparison.R 
    - calculate pairwise Sign and Wilcoxon Sign Rank tests to compare within DRM differences in ARI from different distance metric/IVM pairings.
    - **note:** this should probably be refactored to output a csv 
- 08-05_dbscan_seu-vrc_pairwise_tests.R 
    - Calculate pairwise Sign and Wilcoxon Sign Rank tests to compare between DRM differences in ARI when using SEU-VRC optimized clusterings.
- 08-06_dbscan_seu-vrc_pairwise_heatmaps.py 
    - intputs: `writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods.csv`,`writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods_filtered.csv`,
    `writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods.csv`, `writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods_filtered.csv` 
    - **note:** check which script produce these csvs -- probably dbscan_seu-vrc_pairwise_tests.R
    - used in Figure 6
- 08-07_dbscan_vs_ivm_analysis.R 
    - plots mean/meadian rank of DRM in the IVM analysis vs DBSCAN analysis -- also calculate 
- 08-08_dbscan_barplots.R 
    - output barplots of correlation of ARI from DBSCAN optimization with dataset properties `n_classes`, `n_samples`, `min_class_perc`,
    `max_class_perc`, `protocol`.

Step 09 -- Resource Analysis
----------------------------
- 09-00_get_resource_results.sh 
    - parse through the log files to get time and memory information for each embedding
- 09-01_plot_resources.R 
    * create some plots for memory/time usage
