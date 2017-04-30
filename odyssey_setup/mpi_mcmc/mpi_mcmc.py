#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Baseline mpi MCMC implementations
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np
#import pymc3 as pm
from gaussian_mixture_grid import GaussianMixtureGrid
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

#PARAMETERS
N_SAMPLES = 2**16
N_SAMPLES_PER_PROCESSOR = N_SAMPLES / size
N_DIM = 10
TELEPORTATION_PROB = 0.01

if rank == 0:
    start_time = time.clock()
    print "Running mpi mcmc with teleportation"
    print "Total number of samples", N_SAMPLES
    print "Number of nodes", size

#Setup Grid
grid10d = GaussianMixtureGrid(length=2, dimensionality=N_DIM, spacing=25, stddev=4)

#Run Metropolis-Hastings sampling
samples, indexes = grid10d.mh_with_teleportation(num_samples=N_SAMPLES_PER_PROCESSOR, teleprob=TELEPORTATION_PROB, rejn=N_SAMPLES_PER_PROCESSOR / 4)

#Gather results to node 0
all_samples = None
all_indexes = None
if rank == 0:
    all_samples = np.empty([size, N_SAMPLES_PER_PROCESSOR, N_DIM], dtype = np.float64)
    all_indexes = np.empty([size, N_SAMPLES_PER_PROCESSOR], dtype = np.int64)

comm.Gather(samples, all_samples, root=0)
comm.Gather(indexes, all_indexes, root=0)
#comm.Barrier()

#Write samples to npy file
if rank == 0:
    print "Merged Shape", all_samples.shape
    np.save("samples{}d{}processors.npy".format(N_DIM, size), all_samples)
    np.save("indexes{}d{}processors.npy".format(N_DIM, size), all_indexes)
    print "Elapsed Time", time.clock() - start_time

MPI.Finalize()