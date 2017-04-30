#!/bin/bash
#SBATCH -J mpi_mcmc1
#SBATCH -o mpi_mcmc1.out
#SBATCH -e mpi_mcmc1.err
#SBATCH -p seas_iacs
#SBATCH -n 1
#SBATCH -t 0-1:30
#SBATCH --mem-per-cpu=8000

source new-modules.sh
module load python/2.7.13-fasrc01
source activate cs205project
srun -n $SLURM_NTASKS --mpi=pmi2 python mpi_mcmc_serial.py