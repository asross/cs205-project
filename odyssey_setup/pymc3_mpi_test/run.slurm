#!/bin/bash
#SBATCH -J mpi_pymc
#SBATCH -o mpi_pymc.out
#SBATCH -e mpi_pymc.err
#SBATCH -p seas_iacs
#SBATCH -n 8
#SBATCH -t 30
#SBATCH --mem-per-cpu=2000

source new-modules.sh
module load python/2.7.13-fasrc01
source activate cs205project
srun -n $SLURM_NTASKS --mpi=pmi2 python pymc3_mpi_test.py
