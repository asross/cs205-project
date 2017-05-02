First, using MPI (code [here](https://github.com/asross/cs205-project/blob/master/odyssey_setup/mpi_mcmc/mpi_mcmc.py), we find we are able to run many, many parallel chains (up to 128) simultaneously, achieving strong scaling:

![mpi-conv](mpi-conv.png)
![mpi-ss1](mpi-strong-scale1.png)
![mpi-ss2](mpi-strong-scale2.png)

These are just results for the naive parallel case using MPI. To make it hybrid, we considered using both OpenMP (code [here](https://github.com/asross/cs205-project/blob/master/odyssey_rejection_sampling/openmp_dir/openmp.c)) and OpenAcc (code [here](https://github.com/asross/cs205-project/blob/master/odyssey_rejection_sampling/openacc_dir/openacc.cpp)):

![openaccmp](openaccmp.png)

Although OpenACC is clearly somewhat faster, we settled on OpenMP for two reasons:

1. Generating random numbers within kernels is non-trivial. A naive approach would have each thread spin random numbers off a different seed. However, some random number generators fail to give independent sequences with different seeds which is particularly problematic when so many threads are involved. CUDA offers cuRAND to deal with randomness in a sophisticated manner and a bare bones implementation of rejection sampling using cuRAND is available in the repo. However with OpenACC the convention is to generate random numbers on the host and pass them to the device. This leads to increased communication overhead in terms of memory and time and impairs gains from harnessing the GPU.

2. Ease of integration with the Python framework (which housed the rest of our code).

Below are our full hybrid results for speedup:

![insert Shawn's stuff here once he turns them from raw data into a plot](hybrid-results.png)

This plot is for 16 total processors/nodes which we allocate between MPI and OpenMP. The lowest runtime (the first dot) is when we allocate all of our processing power to OpenMP, suggesting that OpenMP is giving us the most bang for its buck on Odyssey. Clearly, given infinite parallel resources, we should use both OpenMP and MPI.
