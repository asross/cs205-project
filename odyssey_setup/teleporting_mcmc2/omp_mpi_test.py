#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Teleporting MCMC for mpi + omp on Odyssey
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np
import pyximport
pyximport.install()
import sample
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

#############################################################
N_SAMPLES = 2**24
N_SAMPLES_PER_MPI_NODE = N_SAMPLES / size
CHAIN_LENGTH = 2**6 #inverse of teleportation frequency
N_CHAINS = N_SAMPLES_PER_MPI_NODE / CHAIN_LENGTH

if rank == 0:
    start_time = time.clock()
    print "Running mpi+omp mcmc with teleportation"
    print "Total number of samples", N_SAMPLES
    print "Number of MPI nodes", size
    print "Chain length", CHAIN_LENGTH

#initialize random seed (otherwise each node will generate same samples)
sample.random_seed(rank)

# parallel rejection sampling with OpenMP
print "Starting Rejection Sampling", rank
starts = np.empty(N_CHAINS, dtype=np.float64)
sample.rejection(N_CHAINS, starts)

# parallel MCMC sampling with OpenMP
print "Starting MCMC", rank
samples = np.empty((N_CHAINS, CHAIN_LENGTH), dtype=np.float64)
sample.metropolis(N_CHAINS, CHAIN_LENGTH, starts, samples)
samples = samples.flatten("F")

print "Merging Samples", rank
#Gather results to node 0
all_samples = None
if rank == 0:
    all_samples = np.empty([size, N_SAMPLES_PER_MPI_NODE], dtype = np.float64)

comm.Gather(samples, all_samples, root=0)

#Write samples to npy file
if rank == 0:
    all_samples = all_samples.flatten("F")
    np.save("samples1d{}mpinodes.npy".format(size), all_samples)
    print "Elapsed Time", time.clock() - start_time

MPI.Finalize()