#!/bin/bash

#SBATCH --job-name=concat-clicks
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem 64GB
#SBATCH --time=15:00

source ${HOME}/.bashrc
mamba activate baidu-user-annotator-agreement

python main.py concat-clicks
