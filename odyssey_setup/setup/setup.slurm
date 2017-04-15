#!/bin/bash
#SBATCH -J envsetup
#SBATCH -p seas_iacs
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-01:00
#SBATCH --mem 2000
#SBATCH -o envsetup%j_%N.out
#SBATCH -e envsetup%j_%N.err

#Echo Commands
set -x

#Load Modules
source new-modules.sh
module load python/2.7.13-fasrc01

if [ -d "~/.conda/envs/cs205project" ]; then
  echo "cs205project environment already exists!"
else
  echo "Creating cs205project environment"
  conda create --name cs205project --clone="$PYTHON_HOME"
  source activate cs205project
  conda install -c conda-forge pymc3
  conda install -c conda-forge mpi4py=2.0.0
fi
