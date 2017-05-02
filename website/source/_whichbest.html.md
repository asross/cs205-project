The short answer? It depends (especially on dimensionality):

![whichbest](which-meth-best.png)

These results are for a grid with \\(2^\text{number of dimensions}\\) modes with a grid spacing of 25, and with each mode having a standard deviation of 4. Our teleporting algorithm is always at least as good as the best method, but it's not until we reach very high dimensions -- 9, which corresponds to \\(2^9=512\\) modes -- that it starts to outperform both the metropolis and rejection samplers.

Those were plots for individual chains, but the main item of interest is how the results change with parallelism. Let's examine how the number of iterations until we reach a particular level of convergence (implementation details [below](#results-conv)) changes as we vary the number of _parallel_ runs (note: these results are using our naive parallel implementation that does not parallelize the rejection sampling portion):

![time2tol](time2tol.png)

From these plots, the advantage of the teleporting sampler is clear, but what is also interesting is the difference in scaling behavior between the teleporting sampler and unaided Metropolis-Hastings (as well as how it varies with the tolerance). Because of the independence of its samples, rejection sampling is better able to exploit parallel resources even though its efficiency at 9 dimensions is only \\(\approx 0.0008\\) -- less than one tenth of one percent. Metropolis isn't significantly helped by having more parallel chains because each chain is individually biased; they need to reach a minimum length before they fully contribute. Our teleporting sampler appears to get the best of both worlds; it only needs to rejection sample about every 100 iterations, but it's fairly unbiased, so it scales well.

When we need to reach a higher degree of precision, Metropolis-Hastings starts doing a little better compared to rejection sampling, even though the gap does start narrowing as we increase \\(p\\). Perhaps this is because the number of iterations per chain is several orders of magnitude higher, so each chain is closer to mixing.
