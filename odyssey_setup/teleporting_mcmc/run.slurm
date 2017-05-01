#!/bin/bash
#SBATCH -J omp_mpi
#SBATCH -o omp_mpi.out
#SBATCH -e omp_mpi.err
#SBATCH -p seas_iacs
#SBATCH -n 2
#SBATCH -c 4
#SBATCH -t 10
#SBATCH --mem-per-cpu=1000

source new-modules.sh
module load python/2.7.13-fasrc01
source activate cs205project

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
srun -n $SLURM_NTASKS --cpus-per-task=$SLURM_CPUS_PER_TASK --mpi=pmi2 python omp_mpi_test.py