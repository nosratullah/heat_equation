import numpy as np
import scipy as sp
import scipy.linalg as la
import matplotlib.pyplot as plt
import time
from scipy import sparse
import  scipy.sparse.linalg as spla

tLeft = 100 #Tempreture of first element
tRight = 0 #Tempreture of last element
intervals = 100 #number of intervals to mesh the length
alpha = 0.1 #alpha constant
#this part aims to creat a tridiagonal matrix
coeffMat = np.zeros((intervals,intervals)) #making the coefficent matrix
diameter0 = np.ones(intervals)*(1+2*alpha) #diagonal matrix
diameter1 = np.ones(intervals)*(-1*alpha) #diagonal matrix
diagonalMat0 = np.diag(diameter0).reshape((intervals,intervals))
diagonalMat = np.diag(diameter1).reshape((intervals,intervals))
diagonalMat1 = np.roll(diagonalMat,1)
diagonalMat2 = np.roll(diagonalMat, -1)
coeffMat = diagonalMat0 + diagonalMat1 + diagonalMat2
sparsCoeffMat = sparse.coo_matrix(coeffMat)
##############################################
#initial tempreture of the line
knownTemp = np.zeros(intervals)
knownTemp[0] = tLeft
knownTemp[99] = tRight
#finial tempreture of the line
unknownTemp = np.zeros(intervals)
n = 0 #some constant to make png sequences
for i in range(0,20000):
    #unknownTemp = la.solve(coeffMat,knownTemp) #solving linear algebra Ax = b with scipy library
    unknownTemp = spla.spsolve(sparsCoeffMat, knownTemp)
    knownTemp[1:intervals-2] = unknownTemp[1:intervals-2] #giving the finial matrix values to initial matrix to start one more period
    if (i%100==0): #to reduce the number of plots for every 100 loops
        n += 1
        #to create an animation
        plt.cla()
        plt.title('1D Heat Equation')
        plt.xlabel('intervals')
        plt.ylabel('Tempreture')
        plt.plot(unknownTemp,'r-.',label='heat distribution')
        plt.legend(loc='upper right')
        plt.savefig('gif/heatEq{}.png'.format(n))
        plt.pause(0.01)
        time.sleep(0.01)

plt.show()
