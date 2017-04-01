#!/usr/bin/python
#Metropolis-Hasting algorithm

#support both python 2/3 (at least for the most part)
from __future__ import (absolute_import, division, print_function, unicode_literals)
import sys
if sys.version_info[0] == 2:
    range = xrange

#imports
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import time

#note: you must burn samples manually
def metropolis_hastings(prob, proposal, initial_value, num_samples):
	samples = np.empty((num_samples, initial_value.shape[0]))
	x = initial_value
	px = prob(x)

	for i in range(num_samples):
		x_candidate = proposal(x)
		pxc = prob(x_candidate)
		if np.random.random_sample() * px < pxc:
			samples[i,:] = x_candidate
			px = pxc
			x = x_candidate
		else:
			samples[i,:] = x

	return samples

def plot_1D_samples(distribution):
	proposal = lambda x: np.random.normal(x, 1)
	start_time = time.time()
	samples = metropolis_hastings(distribution.pdf, proposal, np.array([0]), 30000)
	print("Time", time.time() - start_time)

	#burn 1000 samples
	samples = samples[1000:]

	plt.figure()
	# histogram of samples
	n, bins, patches = plt.hist(samples.flatten(), 50, normed=True)
	# actual pdf
	plt.plot(bins, distribution.pdf(bins), 'r--', linewidth=1)
	plt.show()

np.random.seed(0)
plot_1D_samples(stats.norm(loc=0, scale=1))
plot_1D_samples(stats.norm(loc=5, scale=0.2))
plot_1D_samples(stats.beta(2,4))
plot_1D_samples(stats.expon())