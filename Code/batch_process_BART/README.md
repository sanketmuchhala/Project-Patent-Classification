This folder contains 4 files:

1. coordinate_sbatches.sh
2. bart_batch_definition.txt
3. run_BART.slurm
4. run_BART_script.py

These files are listed in hierarchical order:

* coordinate_sbatches.sh is the "master" script that runs/utilizes all the others
* bart_batch_definition.txt is a manually created file that defines three columns: 1) Batch Index (limited to indexes less than 100), 2) Start Index, 3) End Index (exclusive). This file was created after testing processing times to see how many batches would be required to process data under the 2-day limit IU HPC team sets.
* run_BART.slurm is executed by coordinate_sbatches.sh for each row of the bart_batch_definition.txt file. Each of the three values in the bart_batch_definition.txt file are passed as parameters to this slurm script
* run_BART_script.py is executed by the run_BART.slurm script with the three parameters from bart_batch_definition.txt file
	* This run_BART_script.py file contains a "folder" parameter that may need updated to reflect the folder in your environment where all of these files are located
	* This script also assumes 2 files are in the "folder" parameter:
		1. naics4.pkl - A pickle file that has the 4-digit NAICS labels we use for zero-shot classification
		2. patents_h2_2020.csv
	* The patents_h2_2020.csv file is just patents data, but it was too large to fit in Github so wasn't included, you may need to download this separately from Basecamp or create your own patents data file to match
