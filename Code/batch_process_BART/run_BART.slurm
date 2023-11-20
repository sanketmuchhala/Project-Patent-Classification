#!/bin/bash

#SBATCH -J BART_patents
#SBATCH -N 1
#SBATCH -A general
#SBATCH -p gpu
#SBATCH -o output_%j.txt
#SBATCH -e errors_%j.err
#SBATCH --gpus 1
#SBATCH --time=23:00:00
#SBATCH --mem=740G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jmonser@iu.edu
#SBATCH --ntasks=2
#SBATCH --ntasks-per-gpu=2

#Load any modules that your program needs
module load deeplearning

# Install required python libraries
#pip install transformers datasets torch --user

#Run your program
srun python run_BART_script.py $1 $2 $3
