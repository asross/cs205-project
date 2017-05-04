The different phases in our parallelization of the problem are illustrated by this diagram:

![odyscheme](odyssey-setup.png)

Our strategy for moving from a serial (top-left) to parallel implementation (bottom-right) is illustrated as follows. Lines represent nodes, webs represent processors.

Teleporting MCMC consists of two alternating sampling strategies; rejection sampling (red) and Markov chain Monte Carlo (blue). We distribute work across processors using:

- OpenMP (via Cython) for rejection sampling; and
- PyMC3's native support for multiple jobs for Hamiltonian MC.

We distribute work across nodes using MPI, specifically using [mpi4py](http://mpi4py.scipy.org/). Naive parallel code is available [here](https://github.com/asross/cs205-project/blob/master/odyssey_setup/mpi_mcmc/mpi_mcmc.py), and our hybrid code (with test cases) is [here](https://github.com/asross/cs205-project/tree/master/odyssey_setup/teleporting_mcmc2). We also tested using OpenAcc and CUDA for GPU-based parallel rejection sampling, which can be seen [here](https://github.com/asross/cs205-project/tree/master/odyssey_rejection_sampling). Note that thorough testing is slightly less important for us because we evaluate our code via [convergence metrics](#results-conv), which implicitly test correctness.
