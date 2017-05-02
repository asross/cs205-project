Evaluating convergence is nontrivial because of the very same multimodality
that makes our datasets difficult to sample. For our mixture of Gaussians, we
take the following approach.

We begin with an array of samples and corresponding iteration indexes. The
iteration index is not implied by the sample ordering because we may have
discarded rejection samples in between final samples in our chain. If we have
multiple parallel chains, we combine samples by mergesorting indexes.

We then take running averages across each sample dimension using a fast
implementation of `cumsum` (cumulative sum) and dividing by the index in the
array. This gives us an array of the cumulative sample average in each
dimension at each iteration.

We then subtract the overall mean of the mixture of Gaussians from the running
sample averages and take the absolute value. This gives us absolute errors for
each dimension at each iteration. Finally we sum across dimensions to obtain a
total error by iteration.

From the central limit theorem, we know that the expected error of estimating
a true mean from a mean across \\(N\\) samples should be

$$
\text{Mean estimation error}(N) = \frac{\sigma}{\sqrt{N}}
$$

If we take this to log-log space, then this becomes:

$$
\log(\text{Mean estimation error}(N)) = \log(\sigma) - \frac{1}{2}\log(N)
$$

This suggests that if we do a linear regression (in log-log space) to the log
error vs. the number of iterations, like this:

![err-by-iter](err-by-iter.png)

then we should obtain a slope of around -0.5 and an intercept that corresponds
to the inherent variance of both the distribution and the sampling method. As
expected, across sampling methods and independent trials, we see a clustering
of slopes around -0.5:

![slope-clust](slope-clust.png)

This suggests that we're following the central limit theorem, and we can
somewhat justifiably take the linear intercept \\(\log(\sigma)\\) as a measure
of how poorly we are converging. This quantity on its own is not that
interpretable (although we could interpret it as the expected log error at 1
sample), but by comparing how it changes as we vary parallelism, we can
generate speedup plots like the ones above and this one below:

![speedup-comp](speedup-comp.png)

However, we can also use our power law fit to simply extrapolate the
time/iterations required to reach a specified convergence, which we do
elsewhere.
