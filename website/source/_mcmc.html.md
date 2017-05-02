MCMC is a _local_ method for sampling from distributions \\(s(x)\\). One of its
simplest forms is the Metropolis-Hastings algorithm, which works as follows.
Assuming you begin at a point \\(x_1\\), you then propose a point \\(x_2\\) by
sampling from a symmetric proposal distribution \\(p(x)\\). You then either
move there or stay put, and add your current location to the sample chain. The
important point is that the ratio of probability of transitioning from
\\(x_1\\) to \\(x_2\\) and back again must equal the ratio of the target
densities \\(s(x_1)\\) and \\(s(x_2)\\). If this condition (called "detailed
balance") holds, then the sample chain will converge to the true distribution.

We can write out detailed balance as follows:

$$
\frac{\text{prob of }x_1\to x_2}{\underbrace{\text{prob of }x_2\to x_1}_{\text{must eq. $s(x_1)/s(x_2)$}}} = \frac{p(x_1|x_2)s(x_1)}{\underbrace{p(x_2|x_1)}_{=\, p(x_1|x_2)}s(x_2)} = \underbrace{\frac{s(x_1)}{s(x_2)}}_{\text{balanced}}
$$

Where we relied on using a symmetric proposal
distribution\\(p(x)\\), though there are ways of using
nonsymmetric proposals. Regardless, MCMC, as a local method,
suffers with multimodality (or in general any non-convex
density \\(s(x)\\)), as its local stepping can get stuck in
local modes:

![something illustrating local modes](mh-trace.png)

These results are for Metropolis-Hastings, which is a relatively simple MCMC
technique, but even Hamiltonian Monte Carlo, the state of the art, gets stuck
in similar ways:

![something illustrating local modes for HMC](HMC-trace.png)

The crux of the problem is that for MCMC to converge, the underlying
distribution must be _ergodic_. Ergodicity is a complex concept but it
intuitively corresponds to reachability; every place in the distribution must
be reachable from any other via entirely local movements. A mixture of
Gaussians like the one from which we sample above technically is ergodic,
because the density is never truly 0 anywhere, but practically is only barely
so. When our distribution is not ergodic or not ergodic enough, our MCMC
samples will be inherently biased.

Because of this inherent bias, MCMC can take impractically many iterations to
converge, and furthermore, the way its convergence speeds up when combining
results from multiple parallel chains is not ideal:

![mcmc-scaling](mcmc-scaling.png)

However, MCMC's advantage is that it scales well with dimensions in terms of
generating lots of samples (even if they are biased). So while MCMC may take a
long time to converge, when it does finally converge, you'll have a lot of
samples.
