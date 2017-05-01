from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, srand, RAND_MAX
#note: we must rename the c math functions. Otherwise, it appears that
#the python version is used and the program hangs/deadlocks with no
#error message when run without GIL
from libc.math cimport exp as c_exp, sqrt as c_sqrt, log as c_log, sin as c_sin, cos as c_cos, M_PI

######################## PRIVATE UTILITIES #################################
#normalization constants
cdef double TWOPI = 2 * M_PI
cdef double ISQRTTWOPI = 1.0 / c_sqrt(TWOPI)

#random double in 0 to 1 range
cdef inline double rand_uniform() nogil:
	return float(rand()) / RAND_MAX

#random double in given range
cdef inline double rand_double(double min_value, double max_value) nogil:
	return (max_value - min_value) * rand_uniform() + min_value

#log pdf of normal without normalization constant (MCMC only cares about ratio)
cdef inline double logp(double x, double mu, double sigma) nogil:
	cdef double z = (x - mu) / sigma
	return -0.5 * z * z

#pdf of normal distribution
cdef inline double normal_pdf(double x, double mu, double sigma) nogil:
	return ISQRTTWOPI * c_exp(logp(x, mu, sigma)) / sigma

#random sample from normal(0, 1)
#see https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform
#note this is slightly wasteful as it only uses one of the 2 values
cdef double rand_normal() nogil:
	cdef:
		int i1
		double u1, u2
	i1 = 0
	while i1 == 0: #catch the edgecase of log 0
		i1 = rand()
	u1 = float(rand()) / RAND_MAX
	u2 = rand_uniform()
	return c_sqrt(-2.0 * c_log(u1)) * c_cos(TWOPI * u2)

#############################################################################
#set the random seed - should be called with separate seed for each MPI node
cpdef void random_seed(unsigned int seed):
	srand(seed)

#box-muller sampling of normal(0, 1) -- exposed for testing
#inputs: number of samples and an empty numpy array to store results
@boundscheck(False)
@wraparound(False)
cpdef void normal_bm(int n_samples, np.float64_t[:] samples) nogil:
	cdef int i
	for i in prange(n_samples, schedule="guided"):
		samples[i] = rand_normal()

#rejection sample from standard normal distribution
#inputs: number of samples and an empty numpy array to store results
@boundscheck(False)
@wraparound(False)
cpdef void normal(int n_samples, np.float64_t[:] samples) nogil:
	cdef:
		double x, y, z
		int i, reject

	for i in prange(n_samples, schedule="guided"):
		reject = 1
		while reject:
			x = rand_double(-3.0, 3.0)
			y = rand_uniform()
			z = normal_pdf(x, 0, 1)
			reject = y > z
		samples[i] = x

#perform parallel metropolis-hastings
#n_starts: number of chains
#n_samples: number of samples per chain
#starts: np array of starts
#samples: n_starts x n_samples array to store results
@boundscheck(False)
@wraparound(False)
cpdef void normal_mh(int n_starts, int n_samples, np.float64_t[:] starts, np.float64_t[:,:] samples) nogil:
	cdef:
		#x value, candidate x value, and corresponding log probabilties
		double x, xc, lpx, lpxc
		int i, j
	for i in prange(n_starts):
		x = starts[i]
		lpx = logp(x, 0, 1)
		for j in range(n_samples):
			xc = x + 0.2 * rand_normal()
			lpxc = logp(xc, 0, 1)
			if rand_uniform() < c_exp(lpxc - lpx):
				x = xc
				lpx = lpxc
			samples[i,j] = x