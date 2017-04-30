from cython cimport boundscheck, wraparound
from cython.parallel import prange
import numpy as np
cimport numpy as np

#parallel summation
@boundscheck(False)
@wraparound(False)
cpdef long long sum_parallel(np.int32_t[:] arr) nogil:
    cdef:
        long long i, total
    total = 0
    #guided seems to give the best performance
    for i in prange(arr.shape[0], schedule="guided"):
        total += arr[i]
    return total