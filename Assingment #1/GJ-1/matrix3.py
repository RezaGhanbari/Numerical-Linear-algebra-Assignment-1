from numpy import array, zeros, float, dot
from copy import copy
import scipy.linalg
import numpy
import time

def GaussJordan(A,b):

    n,m = A.shape
    C = zeros((n,m+1),float)
    C[:,0:n],C[:,n] = A, b

    for j in range(n):
        # partial pivoting.
        p = j
        # look for alternate pivot by searching for largest element in column
        for i in range(j+1,n):
            if abs(C[i,j]) > abs(C[p,j]): p = i
        if abs(C[p,j]) < 1.0e-16:
            print "matrix is singular" # its determinant is 0.
            return b
        # swap rows to get largest magnitude element on the diagonal
        C[p,:],C[j,:] = copy(C[j,:]),copy(C[p,:])

        pivot = C[j,j]
        C[j,:] = C[j,:] / pivot
        for i in range(n):
            if i == j: continue
            C[i,:] = C[i,:] - C[i,j]*C[j,:]
    I,x = C[:,0:n],C[:,n]
    return x

if __name__ == '__main__':

    A = array([[1e-20,0.,1.],
                  [1,1e+20,1.],
                  [0,1,-1],
                  ])
    b = array([0, 1, 1])

    print "A : \n", A
    print "b : \n", b
    x = GaussJordan(A,b)
    print "x: \n", x
    print "Ax : \n", dot(A,x)

    print '\n\nresidual', scipy.linalg.norm(numpy.dot(A, x) - b)/scipy.linalg.norm(A)
    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)