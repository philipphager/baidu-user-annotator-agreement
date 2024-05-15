#!/bin/bash

#SBATCH --job-name=parse-annotations
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --mem 8GB
#SBATCH --cpus-per-task=4
#SBATCH --time=02:00

echo "Data: $1"

source ${HOME}/.bashrc
mamba activate baidu-user-annotator-agreement

python main.py parse-annotations --in-directory=$1
