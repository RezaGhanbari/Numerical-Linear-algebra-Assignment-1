import numpy as np
from scipy.linalg import lu, inv
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
    A = np.array([[1.,1+0.5e-15,3.],
                  [2.,2.,20.],
                  [3.,6.,4.],
                  ])
    b = np.array([1,6,13])
    x = gausselim(A, b)
    print x

    print '\n\nresidual', scipy.linalg.norm(numpy.dot(A, x) - b)/scipy.linalg.norm(A)
    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)