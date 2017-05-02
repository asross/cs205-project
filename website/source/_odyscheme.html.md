The different phases in our parallelization of the problem are illustrated by this diagram:

![odyscheme](odyssey-setup.png)

Our strategy for moving from a serial (top-left) to parallel implementation (bottom-right) is illustrated as follows. Lines represent nodes, webs represent processors.

Teleporting MCMC consists of two alternating sampling strategies; rejection sampling (red) and Markov chain Monte Carlo (blue). We distribute work across processors using:

- OpenMP for rejection sampling; and
- PyMC3's native support for multiple jobs for Hamiltonian MC.

We distribute work across nodes using MPI.
