import numpy as np
import time
import scipy.linalg

def GENP(A, b):

    n =  len(A)
    if b.size != n:
        raise ValueError("Invalid argument", b.size, n)
    for pivot_row in xrange(n-1):
        for row in xrange(pivot_row+1, n):
            multiplier = A[row][pivot_row]/A[pivot_row][pivot_row]
            A[row][pivot_row] = multiplier
            for col in xrange(pivot_row + 1, n):
                A[row][col] = A[row][col] - multiplier*A[pivot_row][col]

            b[row] = b[row] - multiplier*b[pivot_row]
    print A
    print b
    x = np.zeros(n)
    k = n-1
    x[k] = b[k]/A[k,k]
    while k >= 0:
        x[k] = (b[k] - np.dot(A[k,k+1:],x[k+1:]))/A[k,k]
        k = k-1
    return x


def GEPP(A, b):

    n =  len(A)
    if b.size != n:
        raise ValueError("Invalid argument", b.size, n)

    for k in xrange(n-1):
        maxindex = abs(A[k:,k]).argmax() + k
        if A[maxindex, k] == 0:
            raise ValueError("singular")
        #Swap rows
        if maxindex != k:
            A[[k,maxindex]] = A[[maxindex, k]]
            b[[k,maxindex]] = b[[maxindex, k]]
        for row in xrange(k+1, n):
            multiplier = A[row][k]/A[k][k]

            A[row][k] = multiplier
            for col in xrange(k + 1, n):
                A[row][col] = A[row][col] - multiplier*A[k][col]

            b[row] = b[row] - multiplier*b[k]
    print A
    print b
    x = np.zeros(n)
    k = n-1
    x[k] = b[k]/A[k,k]
    while k >= 0:
        x[k] = (b[k] - np.dot(A[k,k+1:],x[k+1:]))/A[k,k]
        k = k-1
    return x

if __name__ == "__main__":
    A = np.array([[1.,1.,3.],
                  [2.,2.,20.],
                  [3.,6.,4.],
                  ])
    b =  np.array([[1.],[6.],[13.]])
    print GENP(np.copy(A), np.copy(b))
    print GEPP(A,b)
    print '\n\nresidual', scipy.linalg.norm(np.dot(A, GEPP(A,b)) - b)/scipy.linalg.norm(A)
    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)
