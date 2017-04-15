#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Test program for mpi + pymc3 on Odyssey
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np
import pymc3 as pm

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

if rank == 0:
    print "Running test with mpi and pymc3"
    print "Number of nodes", size

#sample model
N_SAMPLES = 200
N_DIM = 3
model = pm.Model()
with model:
    mu1 = pm.Normal("mu1", mu=0, sd=1, shape=N_DIM)
    trace = pm.sample(N_SAMPLES, step=pm.NUTS())

#gather results to node 0
sendbuf = trace.get_values("mu1")
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, N_SAMPLES, N_DIM])

comm.Gather(sendbuf, recvbuf, root=0)

#write samples to npy file
if rank == 0:
    print "Merged Shape", recvbuf.shape
    print "Last Samples from each Node"
    for r in range(size):
        print recvbuf[r, -1, :]
    np.save("samples.npy", recvbuf)

MPI.Finalize()
