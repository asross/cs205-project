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
cdef inline double log_normal_pdf(double x, double mu, double sigma) nogil:
	cdef double z = (x - mu) / sigma
	return -0.5 * z * z

#pdf of normal distribution
cdef inline double normal_pdf(double x, double mu, double sigma) nogil:
	return ISQRTTWOPI * c_exp(log_normal_pdf(x, mu, sigma)) / sigma

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

############################################################################

######################## DISTRIBUTION TO SAMPLE ############################
#create 1D mixture of Gaussians
cdef int N_MODES = 3
cdef double *MEANS = [-3.0, 0.0, 3.0]
cdef double SIGMA = 0.5
cdef double MODE_HEIGHT = ISQRTTWOPI / SIGMA / N_MODES
#rejection sample bounds
cdef double BOUND_LEFT = -5.0
cdef double BOUND_RIGHT = 5.0

cdef double logp(double x) nogil:
	#TODO logsumexp might be more stable?
	cdef double result = 0
	cdef int i
	for i in range(N_MODES):
		result += c_exp(log_normal_pdf(x, MEANS[i], SIGMA))
	return c_log(result)

cdef double pdf(double x) nogil:
	return MODE_HEIGHT * c_exp(logp(x))
############################################################################

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

#parallel rejection sample on gaussian mixture
#inputs: number of samples and an empty numpy array to store results
@boundscheck(False)
@wraparound(False)
cpdef void rejection(int n_samples, np.float64_t[:] samples) nogil:
	cdef:
		double x, y, z
		int i, reject

	for i in prange(n_samples, schedule="guided"):
		reject = 1
		while reject:
			x = rand_double(BOUND_LEFT, BOUND_RIGHT)
			y = rand_double(0, MODE_HEIGHT)
			z = pdf(x)
			reject = y > z
		samples[i] = x

#parallel metropolis-hastings on gaussian mixture
#n_starts: number of chains
#n_samples: number of samples per chain
#starts: np array of starts
#samples: n_starts x n_samples array to store results
@boundscheck(False)
@wraparound(False)
cpdef void metropolis(int n_starts, int n_samples, np.float64_t[:] starts, np.float64_t[:,:] samples) nogil:
	cdef:
		#x value, candidate x value, and corresponding log probabilties
		double x, xc, lpx, lpxc
		int i, j
	for i in prange(n_starts):
		x = starts[i]
		lpx = logp(x)
		for j in range(n_samples):
			xc = x + SIGMA * rand_normal()
			lpxc = logp(xc)
			if rand_uniform() < c_exp(lpxc - lpx):
				x = xc
				lpx = lpxc
			samples[i,j] = x