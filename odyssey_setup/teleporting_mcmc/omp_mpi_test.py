#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Test program for mpi + omp on Odyssey
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np
import pyximport
pyximport.install()
import omptest
import pymc3 as pm
import theano
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

#############################################################
if rank == 0:
    start_time = time.clock()
    print "Running mpi mcmc with teleportation"
    print "Total number of samples", N_SAMPLES
    print "Number of nodes", size

N_JOBS = 1
N_SAMPLES_PYMC3 = 50000 / N_JOBS
N_SAMPLES_REJECTION = 1000
super_trace = []
EPISODES = 3 # an episode is one loop of rejection sampling and hmc
N_SAMPLES_PER_PROCESSOR = (N_SAMPLES_PYMC3 * N_JOBS + N_SAMPLES_REJECTION) * EPISODES

for epi in range(EPISODES):
	# rejection sampling
	a = np.empty(N_SAMPLES_REJECTION, dtype=np.float64)
	omptest.rejection_sample(N_SAMPLES_REJECTION, a)
	
	# pass a rejection sampling guided initialization to pymc3
	warm_start = a[-1]

	# pymc3
	model = pm.Model()
	with model:
	    mu1 = pm.Normal("mu1", mu=0, sd=1, shape=1, testval=warm_start)
	    trace = pm.sample(N_SAMPLES_PYMC3, step=pm.NUTS(), progressbar=True, njobs=N_JOBS)

	super_trace.extend(a)
	super_trace.extend(trace[:]['mu1'].ravel())

super_trace = np.array(super_trace)

#Gather results to node 0
all_samples = None
if rank == 0:
    all_samples = np.empty([size, N_SAMPLES_PER_PROCESSOR], dtype = np.float64)

comm.Gather(super_trace, all_samples, root=0)

#Write samples to npy file
if rank == 0:
    print "Merged Shape", all_samples.shape
    np.save("samples{}d{}processors{}jobs.npy".format(N_DIM, size, N_JOBS), all_samples)
    print "Elapsed Time", time.clock() - start_time

MPI.Finalize()