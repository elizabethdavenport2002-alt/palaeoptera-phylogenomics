#!/bin/bash -l

#SBATCH -e slurm.err
#SBATCH -D ./
#SBATCH --export=ALL
#SBATCH -p nodes
#SBATCH -N 1
#SBATCH -n 12
#SBATCH -t 48:00:00

python genome_download.py 
