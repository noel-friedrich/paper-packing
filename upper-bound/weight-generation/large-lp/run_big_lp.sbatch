#!/bin/bash
#SBATCH --job-name=biglp          # Name of the job
#SBATCH --ntasks=1                # Always 1 for a single MPI rank
#SBATCH --cpus-per-task=16        # Number of CPU cores for Gurobi
#SBATCH --mem-per-cpu=4G          # Memory per core (adjust as needed)
#SBATCH --time=24:00:00           # Walltime (hh:mm:ss)
#SBATCH --output=biglp_%j.log     # Log file (%j = job ID)

##########################################
## Start message with timestamp and job ID
echo "$(date) start ${SLURM_JOB_ID}"
##########################################

# load the needed modules
module load stack/2025-06
module load gcc/8.5.0
module load python/3.11.9
module load gurobi/13.0.0
module load eth_proxy
python3 -m pip install gurobipy
python3 -m pip install numpy

# make sure Gurobi sees all allocated threads
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# run the python script
echo "Running big LP with gurobipy..."
python run_big_lp.py

echo "$(date) end ${SLURM_JOB_ID}"