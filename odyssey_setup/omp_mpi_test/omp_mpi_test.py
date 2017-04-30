#!/usr/bin/env python
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Test program for mpi + omp on Odyssey
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from mpi4py import MPI
import numpy as np

import pyximport
pyximport.install()
import omptest

comm = MPI.COMM_WORLD
size = comm.Get_size()   # Size of communicator
rank = comm.Get_rank()   # Rank in communicator

for i in range(0, size):
    comm.Barrier()
    if rank == i:
        print 'Rank %d out of %d' % (rank, size)
        print MPI.Get_processor_name()
        print omptest.sum_parallel(np.arange(1, 100, dtype=np.int32))

MPI.Finalize()
