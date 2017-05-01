#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Teleporting MCMC for mpi + omp on Odyssey
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np
import pyximport
pyximport.install()
import rejection_sample
import pymc3 as pm
import theano
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

#############################################################
N_SAMPLES = 2**16
N_JOBS = 4
N_SAMPLES_PER_MPI_NODE = N_SAMPLES / size
N_SAMPLES_PER_OMP_THREAD = N_SAMPLES_PER_MPI_NODE / N_JOBS
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
rejection_sample.random_seed(rank)

# rejection sampling with OpenMP
print "Starting Rejection Sampling"
rejection_samples = np.empty(N_SAMPLES_REJECTION, dtype=np.float64)
rejection_sample.normal(N_SAMPLES_REJECTION, rejection_samples)

# array to store samples
super_trace = []

print "Starting MCMC"
# MCMC
for cycle, warm_start in enumerate(rejection_samples):
  # pass a rejection sampling guided initialization to pymc3
  model = pm.Model()
  with model:
    mu1 = pm.Normal("mu1", mu=0, sd=1, shape=1, testval=warm_start)
    trace = pm.sample(CHAIN_LENGTH, step=pm.NUTS(), progressbar=False, njobs=N_JOBS)
  super_trace.extend(trace[:]["mu1"].ravel())

#convert to np array for MPI
super_trace = np.array(super_trace)

print "Merging Samples", super_trace.shape
#Gather results to node 0
all_samples = None
if rank == 0:
    all_samples = np.empty([size, N_SAMPLES_PER_MPI_NODE], dtype = np.float64)

comm.Gather(super_trace, all_samples, root=0)

#Write samples to npy file
if rank == 0:
    print "Merged Shape", all_samples.shape
    np.save("samples1d{}processors{}jobs.npy".format(size, N_JOBS), all_samples)
    print "Elapsed Time", time.clock() - start_time

MPI.Finalize()