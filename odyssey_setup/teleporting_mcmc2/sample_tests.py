#test sampling and plot distributions
import numpy as np
import matplotlib.pyplot as plt
import pyximport
pyximport.install()
import sample

N_SAMPLES = 100000

#Random Seed
sample.random_seed(5)

#Test Box-Muller
samples = np.empty(N_SAMPLES, dtype=np.float64)
sample.normal_bm(N_SAMPLES, samples)

plt.figure()
plt.hist(samples, bins=100)
plt.show()

#Test Rejection Sampling
samples = np.empty(N_SAMPLES, dtype=np.float64)
sample.rejection(N_SAMPLES, samples)

plt.figure()
plt.hist(samples, bins=100)
plt.show()

#Test Metropolis Hastings
N_CHAINS = 100
SAMPLES_PER_CHAIN = N_SAMPLES / N_CHAINS
starts = np.empty(N_CHAINS, dtype=np.float64)
sample.rejection(N_CHAINS, starts)
samples = np.empty((N_CHAINS, SAMPLES_PER_CHAIN), dtype=np.float64)
sample.metropolis(N_CHAINS, SAMPLES_PER_CHAIN, starts, samples)

plt.figure()
plt.hist(samples.flatten(), bins=100)
plt.show()