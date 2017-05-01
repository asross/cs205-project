Evaluating convergence is nontrivial because of the very same multimodality that makes our datasets difficult to sample. For our mixture of Gaussians, we take the following approach.

We begin with an array of samples and corresponding iteration indexes. The iteration index is not implied by the sample ordering because we may have discarded rejection samples in between final samples in our chain. If we have multiple parallel chains, we combine samples by mergesorting indexes.

We then take running averages across each sample dimension using a fast implementation of `cumsum` (cumulative sum) and dividing by the index in the array. This gives us an array of the cumulative sample average in each dimension at each iteration.

We then subtract the overall mean of the mixture of Gaussians from the running sample averages and take the absolute value. This gives us absolute errors for each dimension at each iteration. Finally we sum across dimensions to obtain a total error by iteration:

![err-by-iter](err-by-iter.png)

This error tends to fall like 1 over the iteration squared, consistently with the central limit theorem. Indeed, across sampling methods and independent trials, when we do a power-law fit to the resulting trend, we see a clustering around -0.5:

![slope-clust](slope-clust.png)

However, the multiplicative factor of this power law decay, which in log-log space is the linear intercept, depends on the variance of the mixture model and the extent to which time is "dilated" by the inefficiency of our sampler.

Since we are sampling the same distribution across methods, it makes sense to consider the intercept as the true rate of convergence, which is how we generated the speedup plot below:

![speedup-comp](speedup-comp.png)

However, we can also use our power law fit to extrapolate the time/iterations required to reach a specified convergence, which we do above (TODO link).
