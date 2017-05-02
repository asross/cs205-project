Regardless of whether a symmetric of non-symmetric proposal distribution is
used, MCMC, as a local method, suffers with multimodality (or in general any
non-convex density \\(s(x)\\)), as its local stepping can get stuck in local
modes:

![Metropolis-Hastings](mh-trace.png)

The samples above are from a Metropolis-Hastings sampler, which is a
relatively simple MCMC technique. Note that even after removing the first 10%
of samples from the chain and further thinning the chain by a factor of 10,
there are still very high levels of autocorrelation and the distribution of
samples does not reach all of the actual modes.   However, even Hamiltonian
Monte Carlo, the state of the art, gets stuck in similar ways:

![HMC](HMC-trace.png)

The crux of the problem is that for MCMC to converge, the underlying
distribution must be _ergodic_. Ergodicity is a complex concept but it
intuitively corresponds to reachability; every place in the distribution must
be reachable from any other via entirely local movements. A mixture of
Gaussians like the one from which we sample above technically is ergodic,
because the density is never truly 0 anywhere. However, it is only barely
ergodic. When our distribution is not ergodic or not ergodic enough, our MCMC
samples will be inherently biased.

Because of this inherent bias, MCMC can take impractically many iterations to
converge, and furthermore, the way its convergence speeds up when combining
results from multiple parallel chains is not ideal:

![mcmc-scaling](mcmc-scaling.png)

However, MCMC's advantage is that it scales well with dimensions in terms of
generating lots of samples (even if they are biased). So while MCMC may take a
long time to converge, when it does finally converge, you'll have a lot of
samples.
