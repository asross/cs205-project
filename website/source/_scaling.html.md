Independently of inter-method differences, we can also analyze intra-method
speedups (moving back into linear from log space):

![speedup-comp](speedup-comp.png)

We included some of these results above in the background section because they
felt useful not just as results but as characterizations of the methods
themselves. Essentially, rejection sampling is serving as the gold standard: it
produces uncorrelated samples, and so we should expect near-perfect speedup
(almost equaling \\(p\\)). Metropolis produces highly correlated samples,
so we should expect a much less significant speedup from parallelization. Finally, the teleportation method should be somewhere in between (which it is). Given a particular time vs. parallelism
cost tradeoff, we should be able to choose a cost-optimal \\(\epsilon\\) for
our sampler to reach a particular level of precision.

Why not perfect speedup for rejection sampling? As we explain
[below](#results-conv), these speedups are essentially measuring reduction in a
standard deviation that depends both on the inefficiency of the sampler and on
the underlying variance of the distribution. As we increase \\(p\to\infty\\),
we expect the inefficiency of rejection sampling to go away completely since
the samples are fully iid. However, there will still be an underlying variance
inherent to the _distribution_, which will remain constant -- essentially a
minimum problem size.

We feel there may be interesting theoretical connections between ideas about
overhead in parallel systems to variance in probabilistic ones.
