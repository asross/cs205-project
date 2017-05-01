import numpy as np
import matplotlib.pyplot as plt
import pyximport
pyximport.install()
import omptest
import pymc3 as pm
import theano
import time

t0 = time.clock()

N_JOBS = 1
N_SAMPLES_PYMC3 = 50000 / N_JOBS
N_SAMPLES_REJECTION = 1000
super_trace = []
EPISODES = 3 # an episode is one loop of rejection sampling and hmc

for epi in range(EPISODES):
	# rejection sampling
	a = np.empty(N_SAMPLES_REJECTION, dtype=np.float64)
	omptest.rejection_sample(N_SAMPLES_REJECTION, a)
	
	# pass a rejection sampling guided initialization to pymc3
	warm_start = a[-1]

	# pymc3
	model = pm.Model()
	with model:
	    mu1 = pm.Normal("mu1", mu=0, sd=1, shape=1, testval=warm_start)
	    trace = pm.sample(N_SAMPLES_PYMC3, step=pm.NUTS(), progressbar=True, njobs=N_JOBS)

	super_trace.extend(a)
	super_trace.extend(trace[:]['mu1'].ravel())

runtime = time.clock() - t0
print("runtime for %i pymc3 workers = %0.3f" % (N_JOBS, runtime))

plt.hist(super_trace)
plt.show()





