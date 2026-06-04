#!/bin/bash -l
#SBATCH --job-name=mitigate-social-desirability-bias
#SBATCH --output=logs/%x_%j.out    
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --time=14:00:00
#SBATCH --partition=gpu_mig
#SBATCH --reservation=terv92681

set -euo pipefail

#Add working directory to python path
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

#Gets rid of warnings and progress bars in logs
export TRANSFORMERS_VERBOSITY=error
export HF_HUB_DISABLE_PROGRESS_BARS=1

#Path to local model
export LLAMA_MODEL_PATH="$PWD/Meta-Llama-3.1-8B-Instruct"

#Make sure it runs offline
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1

mkdir -p logs
srun python -u main_mq.py 2020 first original priming
