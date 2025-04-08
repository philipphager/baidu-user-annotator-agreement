#!/bin/bash

#SBATCH --job-name=filter-clicks
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4GB
#SBATCH --time=02:00
#SBATCH --array=1000-2000%50

source ${HOME}/.bashrc
mamba activate baidu-user-annotator-agreement

echo "Data: $1"

python main.py filter-clicks $SLURM_ARRAY_TASK_ID --in-directory=$1
