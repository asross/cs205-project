Rejection sampling is at the opposite end of the spectrum from
Metropolis-Hastings, though it is also quite simple to describe. In rejection
sampling, you essentially draw a giant box enclosing your distribution \\(s\\):

![rej-illust](rej-illust.png)

With psuedocode:

<div class='well' style='font-family: monospace; white-space: pre'><strong>function</strong> RejectionSample(\(s\), N):
  samples = []
  <strong>for</strong> attempt <strong>in</strong> 1...N:
    \(x, y\) \(\sim\) box enclosing \(s\)
    <strong>if</strong> \(y\) < \(s(x)\):
      samples.add(\(x\))
  <strong>return</strong> samples
</div>

For distributions with infinite support, you can use an encapsulating Gaussian
or other analytically samplable distribution in place of a box, or you can
approximate one. In any case, you pick a random location within your enclosing
distribution, then check to see if it falls underneath \\(s\\) at that
location. If so, you accept it, but otherwise, you reject it. Unlike in MCMC,
you discard the rejected samples, and the method is completely global; samples
are exactly from \\(s\\) and entirely uncorrelated with each other (iid).

These properties make rejection sampling quite robust to multimodality. Even with 512
fairly disconnected modes, we see a much better speedup in convergence when
combining samples from multiple rejection samplers:

![rej-scaling](rej-scaling.png)

Furthermore, although MCMC is kind of an inherently sequential algorithm since we must build a chain from location to location, rejection sampling can be parallelized at every level (both across nodes using MPI and within nodes using OpenMP).

However, although rejection sampling can handle multimodality, it can't handle
multidimensionality. The fraction of samples we accept falls exponentially as the number of dimensions is increased (and the underlying distribution becomes ever more sparse.) This relationship is illustrated by this Gaussian mixture example:

![rej-dim-scaling](rej-dim-scaling.png)

From this analysis, we can consider rejection sampling and MCMC as two
different extremes of point-based sampling (and if we use a giant,
\\(s\\)-enclosing proposal distribution for MCMC, they become almost
equivalent). But they have exactly the opposite strengths and weaknesses: MCMC
handles dimensionality well but not multimodality; rejection sampling handles
multimodality well but dimensionality.
