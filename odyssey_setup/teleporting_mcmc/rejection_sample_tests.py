#test rejection sampling and plot distribution
import numpy as np
import matplotlib.pyplot as plt
import pyximport
pyximport.install()
import rejection_sample

N_SAMPLES_REJECTION = 100000
rejection_sample.random_seed(5)

a = np.empty(N_SAMPLES_REJECTION, dtype=np.float64)
rejection_sample.normal(N_SAMPLES_REJECTION, a)

plt.hist(a, bins=100)
plt.show()