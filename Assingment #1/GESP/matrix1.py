from numpy.matlib import *
import numpy
import time
import scipy.sparse.linalg
 
 
def gausselim(A, b, pivoting = 0, ztol = 1.0e-8, debug = False):

    size = len(A)
    x    = [0.0] * size
    R    = range(size)
    C    = range(size)
    code = 0
 
    # Triangularization.
    for pivot in range(size-1):
        absm    = abs(A[pivot][pivot])
        exchrow = pivot
        exchcol = pivot
 
        if pivoting == 1: # partial pivoting.
            for row in range(pivot + 1, size):
                atestm  = abs(A[row][pivot])
                if atestm > absm:
                   absm    = atestm
                   exchrow = row
 
        elif pivoting == 2: #full pivoting.
            for row in range(pivot + 1, size):
                for col in range(pivot, size):
                   atestm  = abs(A[row][col])
                   if atestm > absm:
                      absm    = atestm
                      exchrow = row
                      exchcol = col
 
        elif pivoting == 3: # rook pivoting.
           # find element which is maximum in its row and column
           # but using rook moves (alternating vertical and horizontal directions) only
           # NOT OPTIMIZED YET!   
           absm  = 0.0
           Done = False
           while not Done:
               Done = True
               #Find row with maximum element in column exchcol. 
               for row in range(exchrow, size):
                   atest = abs(A[row][exchcol])
                   if atest > absm:
                      absm  = atest
                      exchrow = row
                      Done = False
 
               #Find col with maximum element in row exchrow.               
               for col in range(pivot, size):
                   atest = abs(A[exchrow][col])
                   if atest > absm:
                      absm = atest
                      exchcol = col
                      Done = False
 
 
        #Exchange columns ? 
        if pivot != exchcol:
            if debug: print "exhanging columns", pivot, exchcol
            for row in range(pivot, size):
                A[row][pivot], A[row][exchcol] = A[row][exchcol], A[row][pivot]
            #B[pivot], B[exchcol] = B[exchcol],B[pivot]
            C[pivot] = exchcol
 
        #Exchange rows?
        if pivot != exchrow:
            if debug: 
               print "Exchanging rows:",  pivot,  exchrow
            A[exchrow],A[pivot] = A[pivot], A[exchrow]
            b[exchrow],b[pivot] = b[pivot], b[exchrow]
            R[pivot] = exchrow
 
        if absm > ztol:
           if debug:
               print "pre reduction for row",pivot 

           m = float(A[pivot][pivot])
           for row in range(pivot +1, size): 
               kmul = float(A[row][pivot])/m 
               # Apply rectangular rule.(Reduction)
               for col  in range(size -1, pivot, -1):
                    A[row][col] = float(A[row][col]) - kmul * A[pivot][col]
               b[row] = float(b[row]) - kmul * b[pivot]
               A[row][pivot] = 0.0
 
           if debug:
               print "post reduction:"
               print
 
        else:        
           code = 1
 
    # Perform Back substitution.
    if debug: 
       print "Back substitution: row, rhs sum, pivot"
    if code == 0:
        for row in range(size-1, -1, -1):
           sum = b[row]
           for k in range(row+1, size):
                sum -= (x[k] * A[row][k])
           #print row, sum, A[row][row]
           x[row] = sum/A[row][row]
        reorder(x,C)
        if debug: print "Computed value of X = ",  x
    return (code,R,C, A,x,b)
 
 
def reorder(x   , C):
    for i, c in enumerate(C):
        if i != c:
           #exchange elements at positions i and c.
           x[i], x[c] =  x[c], x[i]
    return x
 
 
def Solve(A,b):  

    (code, R,C, A, x, b) = gausselim(A, b)
    if code==0:
        return x
    else:
        return None
 
 
if __name__ == "__main__":
    A = [[1,1,3],
        [2,2,20],
        [3,6,4]]
    b =  [1,6,13]

    code, R,C, A,x, b = gausselim(A,b, pivoting=1, debug =True)

    print "X \n", x
    print '\n\nresidual', scipy.linalg.norm(numpy.dot(A, Solve(A, b)) - b)\
                          /scipy.linalg.norm(A)

    tic = time.clock()
    toc = time.clock()
    print "Processing time is : %f" %(toc - tic)