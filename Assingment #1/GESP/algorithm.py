from numpy.matlib import *
import numpy
import time
import scipy.sparse.linalg

 
def gausselim(A, B, pivoting = 0, ztol = 1.0e-8, debug = False):
    
    size = len(A)
    X    = [0.0] * size
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
            B[exchrow],B[pivot] = B[pivot], B[exchrow]
            R[pivot] = exchrow
 
        if absm > ztol:
           if debug:
               print "pre reduction for row",pivot 
               print "current augmented matrix:"
               # mataugprint(A,B)
           m = float(A[pivot][pivot])
           for row in range(pivot +1, size): 
               kmul = float(A[row][pivot])/m 
               # Apply rectangular rule.(Reduction)
               for col  in range(size -1, pivot, -1):
                    A[row][col] = float(A[row][col]) - kmul * A[pivot][col]
               B[row] = float(B[row]) - kmul * B[pivot]
               A[row][pivot] = 0.0
 
           if debug:
               print "post reduction:"
               print "current augmented matrix:"
               # mataugprint(A,B)
               print
 
        else:        
           code = 1
 
    # Perform Back substitution.
    if debug: 
       print "Back substitution: row, rhs sum, pivot"
    if code == 0:
        for row in range(size-1, -1, -1):
           sum = B[row]
           for k in range(row+1, size):
                sum -= (X[k] * A[row][k])
           #print row, sum, A[row][row]
           X[row] = sum/A[row][row]
        reorder(X,C)
        if debug: print "Computed value of X = ",  X
    return (code,R,C, A,X,B)	    
 
 
def reorder(X, C):
    for i, c in enumerate(C):
        if i != c:
           #exchange elements at positions i and c.
           X[i], X[c] =  X[c], X[i]
    return X
 
 
def Solve(A,b):  
    
    (code, R,C, A, X, B) = gausselim(A, b)
    if code==0:
        return X
    else:
        return None

