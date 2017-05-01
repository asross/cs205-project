from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np
from libc.stdlib cimport rand
# cdef extern from "limits.h":
# 	int INT_MAX
# from libc.math cimport sqrt, exp, pow, M_PI
# cdef extern from "<math.h>" nogil:
# 	double exp(double x)
cdef extern from "math.h" nogil:
	double c_exp "exp" (double)

@boundscheck(False)
@wraparound(False)
cpdef void rejection_sample(int n_trials, np.float64_t[:] samples) nogil:
	cdef:
		double x, y, z
		int i

	for i in prange(n_trials, schedule="guided"):
		z = 0
		y = 2

		while y>z:
			x = float(rand()) / 32767 * 4 - 2
			y = float(rand()) / 32767
			z = (2*3.14159265358979)**-0.5 * c_exp(-0.5*x**2)		
		samples[i] = x

	return
