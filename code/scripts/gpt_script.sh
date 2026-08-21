#!/bin/bash -l
#SBATCH --job-name=mitigate-social-desirability-bias-
#SBATCH --output=gptlogs/%x_%j.out    
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --time=14:00:00
#SBATCH --partition=gpu_a100

set -euo pipefail

#Add working directory to python path
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

mkdir -p gptlogs

srun python -u main_mq.py 2020 first original none # replicate
# srun python -u main_mq.py 2020 third reformulated none # reformulated
# srun python -u main_mq.py 2020 first original preamble # preamble
# srun python -u main_mq.py 2020 first original priming # priming

## other year or survey
# srun python -u main_mq.py 2024 first original none # replicate

# srun python -u main_mq_wvs_country.py DEU first original none
