The model we chose to run our experiments against is the Gaussian mixture
model.  This problem is synthetic rather than real-world, but it has the
advantage of being analytically tractable and easy to sample from, so we can
easily evaluate a number of exact rather than approximate convergence metrics.
We describe a major real-world application [later on](#relwork-sens). Here are contour plots
of the density of a 2D, 3x3 Gaussian mixture grid:

![GMM](pdf-and-log-pdf.png)

We implemented a [parameterized class](https://github.com/asross/cs205-project/blob/master/datasets/gaussian_mixture_grid.py) to generate Gaussian mixtures with varying dimensions, spacing, variance, and mode count:

![GMM2](gmixgrid.png)

This gives us the flexibility to increase the multimodality and variance of our distribution while keeping the distribution tractable enough to accurately assess convergence.
