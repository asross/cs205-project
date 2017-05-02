#!/bin/bash 

#SBATCH -p holyseasgpu  #Partition to submit to 
#SBATCH -n 1  #Number of cores 
#SBATCH --gres=gpu
#SBATCH -t 10  #Runtime in minutes
#SBATCH --mem-per-cpu=10000


pgc++ -acc -ta=nvidia -Minfo=accel -o openacc openacc.cpp

./openacc > "out-openacc.txt"
