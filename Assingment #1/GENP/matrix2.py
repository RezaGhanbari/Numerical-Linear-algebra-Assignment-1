"""
In the name of Allah
VCS : Git
Editor : Atom Github
Lang : Python 2.7

"""
import numpy as np
import time
import scipy.linalg

def forward_elimination(A, b, n):
    #pass
    for row in range(0, n-1):
        for i in range(row+1, n):
            factor = A[i,row] / A[row,row]
            for j in range(row, n):
                A[i,j] = A[i,j] - factor * A[row,j]

            b[i] = b[i] - factor*b[row]

        print "A is equals to \n%s and \n b is equals to %s" %(A,b)
    return A, b

def back_substitution(a, b, n):

    x = np.zeros((n,1))
    x[n-1] = b[n-1] / a[n-1, n-1]
    for row in range(n-2, -1, -1):
        sums = b[row]
        for j in range(row+1, n):
            sums = sums - a[row,j] * x[j]
        x[row] = sums / a[row,row]
    return x

# gauss function
def gauss(A, b):

    n = A.shape[0]
    if any(np.diag(A)==0):
        raise ZeroDivisionError(('Division by zero occured; '
                                  'pivoting is not supported!!'))

    A, b = forward_elimination(A, b, n)
    return back_substitution(A, b, n)


# Main program starts here

if __name__ == '__main__':
    A = np.array([[1, 1+0.5e-15, 3],
                  [2, 2, 20],
                  [3, 6, 4]])
    b = np.array([1, 6, 13])
    x = gauss(A, b)
    print('Gauss result is x = \n %s' % x)
    print '\n\nresidual', scipy.linalg.norm(np.dot(A, x) - b)/scipy.linalg.norm(A)
    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)
