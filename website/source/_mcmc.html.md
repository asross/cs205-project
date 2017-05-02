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
distribution \\(p(x)\\), though there are ways of using
non-symmetric proposals.
