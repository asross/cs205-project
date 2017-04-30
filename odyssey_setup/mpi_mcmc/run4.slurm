#!/bin/bash
#SBATCH -J mpi_mcmc4
#SBATCH -o mpi_mcmc4.out
#SBATCH -e mpi_mcmc4.err
#SBATCH -p seas_iacs
#SBATCH -n 4
#SBATCH -t 0-0:30
#SBATCH --mem-per-cpu=2000

source new-modules.sh
module load python/2.7.13-fasrc01
source activate cs205project
srun -n $SLURM_NTASKS --mpi=pmi2 python mpi_mcmc.py