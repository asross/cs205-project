# CS205 Spring 2017 Project

Laith Alhussein, Nathaniel Burbank, Shawn Pan, Andrew Ross, and Rohan Thavarajah

## Project Proposals

### Teleporting Parallel MCMC

Motivation: MCMC samples efficiently but only for ergodic chains, and then only with correlations. Rejection sampling is inefficient even on steroids but generates uncorrelated samples even over multimodal distributions.

Assume we are trying to sample from a target distribution `s(x)` which is not amenable to normal MCMC.

On one set of nodes, we run many parallel copies of an inefficient rejection sampler for `s` that only has a probability `\epsilon` of generating a sample. Whenever we generate a sample, we send it asynchronously via MPI to a shared buffer.

On another set of nodes, we run many parallel copies of an efficient but biased MCMC sampler that normally uses a symmetric proposal `p(x2|x1)` and accepts proposals with probability `min(1, p(x2|x1)s(x2)/p(x1|x2)s(x2)) = min(1, s(x2)/s(x1))`. However, these MCMC samplers are modified to _teleport_ with probability `\epsilon` to a random rejection sample they claim from the shared buffer (which they always accept). We can see that this modified proposal still satisfies detailed balance:

![detailed balance](doc/balance.png)

If a rejection sample is unavailable, we block until one is generated, but because the teleportation probability is related to the rate at which we can generate rejection samples (and because we have many nodes independently generating rejection samples), we are unlikely to be blocked by the unavailability of samples. This process ideally allows us to calculate unbiased expectations using MCMC even though our target distribution is multimodal.

To evaluate this method, we would determine if:
- sampling with teleportation gives more accurate expectations than sampling without, for various proposals and numbers of iterations
- splitting nodes between rejection sampling and MCMC performs better than simply allocating all nodes to one or the other
- there is an ideal ratio / teleportation probability `\epsilon` for a given distribution `s` that determines how we should allocate our nodes

### Hierarchical Parallel MCMC

Imagine a hierarchy of MCMC samplers that propose points at different length scales. We could start with one "global" sampler that may be inefficient but can move long distances across the distribution. This global sampler periodically spawns subsamplers, which movie with a smaller length scale and perhaps have a limited lifespan. These subsamplers can themselves spawn subsubsamplers that explore even more locally for an even shorter period of time. Subsampling tasks can execute in parallel using a (possibly distributed) thread pool, and additional processes can aggregate results.

Analysis and care is needed to ensure that this method gives us unbiased samples in the long run. For example, the lifespan of subsamplers may need to depend on the magnitude of `s(x)` at the `x` from which they are spawned.

To evaluate this method, we would again check to see if we obtain more accurate expectations with less time / computing resources than simple parallel or sequential chains. We would also try to determine if there are good initial length scales and length scale / iteration decays for lower-level sampling.

### Hidden Markov Models for GPU

There are three reasons I think parallelizing HMMs are promising.
1.) HMMs are littered with matrix operations. I believe the forward-backward algorithm in particular can go on the GPU which means we have the potential to realize very large speedup (confirmed via rough literature search).
2.) Readily split between multiple team members. HMMs are associated with a bundle of inferences of interest. For instance most likely path (Viterbi), Baum-Welch (emission and transition matrices) etc. This would naturally lend itself being distributed across the team.
3.) Relatively simple to check our implementation is correct. In particular, if we decide on initialization for EM, the solution is deterministic so we'll get the same result on reruns. It's also easy to generate data with which to test our implementation. Finally HMMs are really fun! 
