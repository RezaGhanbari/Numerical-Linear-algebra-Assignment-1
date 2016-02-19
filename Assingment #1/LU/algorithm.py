import numpy as np
from scipy.linalg import lu, inv

def gausselim(A,B):


    pl, u = lu(A, permute_l=True)

    y = np.zeros(B.size)
    for m, b in enumerate(B.flatten()):
        y[m] = b
        # skip for loop if m == 0
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

