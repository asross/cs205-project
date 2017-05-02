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
N_SAMPLES = 2**16
N_SAMPLES_PER_MPI_NODE = N_SAMPLES / size
N_CHAINS = N_SAMPLES_PER_MPI_NODE / CHAIN_LENGTH
CHAIN_LENGTH = 64 #inverse of teleportation frequency
N_SAMPLES_REJECTION = N_SAMPLES_PER_OMP_THREAD / CHAIN_LENGTH

if rank == 0:
    start_time = time.clock()
    print "Running mpi+omp mcmc with teleportation"
    print "Total number of samples", N_SAMPLES
    print "Number of MPI nodes", size
    print "Number of OMP threads", N_JOBS
    print "Chain length", CHAIN_LENGTH

#initialize random seed (otherwise each node will generate same samples)
sample.random_seed(rank)

# parallel rejection sampling with OpenMP
print "Starting Rejection Sampling"
starts = np.empty(N_SAMPLES_REJECTION, dtype=np.float64)
sample.rejection(N_SAMPLES_REJECTION, starts)

# parallel MCMC sampling with OpenMP
print "Starting MCMC"
samples = np.empty((N_CHAINS, CHAIN_LENGTH), dtype=np.float64)
sample.metropolis(N_CHAINS, CHAIN_LENGTH, starts, samples)
samples = samples.flatten()

print "Merging Samples", samples.shape
#Gather results to node 0
all_samples = None
if rank == 0:
    all_samples = np.empty([size, N_SAMPLES_PER_MPI_NODE], dtype = np.float64)

comm.Gather(samples, all_samples, root=0)

#Write samples to npy file
if rank == 0:
    print "Merged Shape", all_samples.shape
    np.save("samples1d{}processors{}jobs.npy".format(size, N_JOBS), all_samples)
    print "Elapsed Time", time.clock() - start_time

MPI.Finalize()