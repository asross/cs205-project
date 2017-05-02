First, using MPI, we find we are able to run many, many parallel chains (up to 128) simultaneously, achieving strong scaling:

![mpi-conv](mpi-conv.png)
![mpi-ss1](mpi-strong-scale1.png)
![mpi-ss2](mpi-strong-scale2.png)

TODO, possibly: generate a speedup graph from the error traces just to supplement this.

We are also able to speed up our algorithm using our hybrid MPI + OpenMP + multi-process approach (for a simpler, 1D, 3-mode Gaussian mixture):

![hybrid-results](hybrid-results.png)
