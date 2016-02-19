import numpy as np
from scipy.linalg import lu, inv
import scipy
import scipy.linalg
import numpy
import time

def gausselim(A,B):


    pl, u = lu(A, permute_l=True)

    y = np.zeros(B.size)
    for m, b in enumerate(B.flatten()):
        y[m] = b
        if m:
            for n in xrange(m):
                y[m] -= y[n] * pl[m,n]
        y[m] /= pl[m, m]

    x = np.zeros(B.size)
    lastidx = B.size - 1  # last index
    for midx in xrange(B.size):
        m = B.size - 1 - midx  # backwards index
        x[m] = y[m]
        if midx:
            for nidx in xrange(midx):
                n = B.size - 1  - nidx
                x[m] -= x[n] * u[m,n]
        x[m] /= u[m, m]
    return x

if __name__ == '__main__':
    data = np.zeros((100,100))
    data[np.arange(99), np.arange(99)+1] = [-1]
    data[np.arange(99)+1, np.arange(99)] = [-1]
    data[np.arange(100), np.arange(100)] = [-2]
    A = data


    data = np.zeros((100,1))
    data[np.arange(98)+1, np.arange(1)] = [1]
    data[np.arange(1), np.arange(1)] = [2]
    data[np.arange(1)+99, np.arange(1)] = [2]
    b =  data
    x = gausselim(A, b)
    print("x is :")
    print x

    print '\n\nresidual', scipy.linalg.norm(numpy.dot(A, x) - b)/scipy.linalg.norm(A)
    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)