#!/bin/bash -l
#SBATCH --job-name=MLMM-Joint-Publication
#SBATCH --output=llama3170blogs/%x_%j.out    
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=14
#SBATCH --mem=90G
#SBATCH --gpus-per-node=4
#SBATCH --time=28:00:00
#SBATCH --partition=gpu_h100

set -euo pipefail

#Add working directory to python path
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

#Gets rid of warnings and progress bars in logs
export TRANSFORMERS_VERBOSITY=error
export HF_HUB_DISABLE_PROGRESS_BARS=1


#Make sure it runs offline
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1

mkdir -p llama3170blogs
srun python -u main_mq.py 2020 first original none # use common_llama3170b