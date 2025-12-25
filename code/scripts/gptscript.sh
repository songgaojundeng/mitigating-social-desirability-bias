#!/bin/bash -l
#SBATCH --job-name=mitigate-social-desirability-bias
#SBATCH --output=gptlogs/%x_%j.out    
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --time=14:00:00
#SBATCH --partition=gpu_mig
#SBATCH --reservation=terv92681

set -euo pipefail

#Add working directory to python path
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

mkdir -p gptlogs
srun python -u main_mq.py 2024
