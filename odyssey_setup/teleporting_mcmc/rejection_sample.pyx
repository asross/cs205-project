from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand, srand, RAND_MAX
from libc.math cimport exp as c_exp, sqrt as c_sqrt, M_PI

#normalization constant
cdef double NORM = 1.0 / c_sqrt(2 * M_PI)

#random double in given range
cdef inline double rand_double(double min_value, double max_value) nogil:
	return (max_value - min_value) * float(rand()) / RAND_MAX + min_value

#set the random seed
cpdef void random_seed(unsigned int seed):
	srand(seed)

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
			y = rand_double(0.0, 1.0)
			z = NORM * c_exp(-0.5 * x * x)
			reject = y > z
		samples[i] = x