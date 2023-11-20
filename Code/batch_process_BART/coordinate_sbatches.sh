while read -r batchidx startidx endidx; do sbatch run_BART.slurm $batchidx $startidx $endidx; done < bart_batch_definition.txt
