A natural model to compare sampling methods on is a mixture of Gaussians. These
distributions are naturally multimodal, but their full distribution is known
and easy to sample from, so we can easily evaluate a number of exact rather
than approximate convergence metrics. We can also vary the parameters of the
mixture (i.e. the proximity and width of each mode as well as the number of
modes and dimensions) and evaluate how our convergence metrics differ under
these conditions.

![GMM](pdf-and-log-pdf.png)