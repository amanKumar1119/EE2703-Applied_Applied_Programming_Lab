"""
Author     : Aman Kumar
Assignment : 5 Laplace Equation
Date       : 27-03-2021
Inputs     : Nx, Ny, radius(of electrode), Niter(number of iterations)            
Output     : 1. A contour plot of the potential before solving(iterations) Laplace equation
             2. Semilog and loglog plots Errors(max difference) in phi after every iteration w.r.t previous iteration
             3. Semilog and loglog plots of errors calculated by fitting the errors to the equation error(k) = A*exp(B*k)
             4. 3_D surface plot of the potential after solving
             5. A contour plot of the potential after solving(iterations) Laplace equation
             6. Vector Plot of Currents
             7. Plot of net error vs no. of iterations.
Important  : 1. Nx and Ny should be same
             2. Size of plate is 1cm x 1cm
             3. Niter should be greater than 500
             4. radius should be smaller than Nx/2
"""

#Importing important libraries

import pylab as pl                                   #Mainly for plotting
import mpl_toolkits.mplot3d.axes3d as p3             #For 3-D surface plot
import numpy as np                                   #For arrays and some mathemtical functions like exp()
from sys import argv                                 #For taking imput through the command line
#%%
"""
1. Taking inputs for Nx, Ny, radius, Niter
2. If all four of these values are provided through command line then those values are used otherwise default values are used.
"""
if len(argv) == 5:                                   #Checking if 4 arguments are passsed
    Nx = min((int(argv[1]),int(argv[2])))            #If Nx and Ny are different then the minimum of those two is taken as Nx and Ny
    Ny = min((int(argv[1]),int(argv[2])))
    if argv[1] != argv[2]:
        print("Nx and Ny should be equal for my program. If they are not equal, the minimum of the two is taken for both Nx and Ny")
    if int(argv[3]) > Nx/2 :                         #Checking if radius given is not greater than size of plate.
        radius = 8                                   #If it is greater than radius is set to default value
        print("\nRadius given is greater than size of plate. Default value is taken.")
    else:
        radius = int(argv[3])
    if int(argv[4]) > 500:                           #Checking if Niter given is greater than 500. Because in a later part of this program
        Niter = int(argv[4])                         #we are fitting the errors to a function after removing the first 500 elements of errors vector
    else:
        Niter = 1500                                 #In case Niter < 500, it is set to 1500(default value)
        print("Niter cannot be less than 500. It's default value 1500 is taken.")
else:
    print("\nUsage: %s <Nx> <Ny> <radius> <Niter>\nThe default values are taken for parameters." % argv[0])    
    Nx=25                  # size along x
    Ny=25                  # size along y
    radius=8               # radius of central lead
    Niter=1500             # number of iterations to perform

"""
Function to calculate the net error after the estimation of A and B(parameters)
"""
def net_error(A,B):
    return ((-A/B)*np.exp(B*(iter_ + 0.5)))

"""
1. Function to calculate the parameters A and B for the error model
2. It uses the least squares technique to best fit the data to the model
3. The matrix problem is M.p = log(errors)
"""    
def best_fit(N):
    c1 = np.ones((N,1))
    c2 = np.array(range(Niter-N,Niter))
    M = pl.c_[c1,c2]
    p = pl.lstsq(M,np.log(errors[Niter-N:]),rcond = None)
    return(np.exp(p[0][0]),p[0][1])
 
#Declaring important arrays and vectors 
phi = np.zeros((Nx,Ny))                     #Array to store the potential at all nodes of the plate
errors = np.zeros(Niter)                    #Vector to store the errors(max difference) in phi after every iteration w.r.t previous iteration
x = pl.linspace(0.5,-0.5,Nx)                #The plate is (1cm)x(1cm). Thus, x goes from -0.5 to 0.5 cm
y = pl.linspace(0.5,-0.5,Ny)                #y goes from -0.5 to 0.5 cm
X,Y = pl.meshgrid(x,y)

ii = pl.where(X*X + Y*Y <= (radius/Nx)**2)  #Identifying the points within radius of wire.
phi[ii] = 1                                 #Setting those points to 1 V

"""
Plotting the contour plot of the potential before solving(iterations) the Laplace equation
"""
fig0 = pl.figure(0)                                 #Opening a new figure
pl.contourf(X,Y,phi)    
pl.title("Contour Plot of Potential(2D) before solving")
pl.scatter(X[ii],Y[ii],color="red",label="Electrode Nodes")
pl.xlabel("X($cm$)")
pl.ylabel("Y($cm$)")
pl.legend()
pl.colorbar()
pl.show()

"""
The main loop for solving the problems
"""
for k in range(Niter):
    oldphi = phi.copy()                           #Saving current values of potential
    phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[:-2,1:-1] + phi[2:,1:-1])
    phi[ii] = 1
    
    #Boundary conditions.
    phi[1:-1,0] = phi[1:-1,1]                     #Top boundary
    phi[1:-1,-1] = phi[1:-1,-2]                   #Right boundary
    phi[0,1:-1] = phi[1,1:-1]                     #Left boundary
    phi[-1,1:-1] = 0                              #Lower boundary(grounded)
    
    errors[k] = abs(phi - oldphi).max()           #Finding the max difference in phi before and after an iteration
    


k = np.array(range(Niter))                        #array used for plotting
iter_ = np.arange(500,2*Niter,100)                #for doing the net error plot against number of iterations

A_,B_ = best_fit(Niter)                           #Estimating A and B for the entire vector of errors
A,B = best_fit(Niter - 500)                       #Estimating A and B for those error entries after the 500th iteration.

#Calculating Error vector for the two fits respectively
Error_ = A_*(np.exp(B_*k))
Error = A*(np.exp(B*k))

#Printing the estimated values of A and B
print("\nFor entire vector of errors A =",A_,"and B =",B_)
print("For error entries after 500th iteration A =",A,"and B =",B)

#Plotting the actual error vector and the error vectors calculated by the two fits on semilog.
#We are taking every 50th point in the vector.
fig1 = pl.figure(1)
pl.semilogy(k[::50],errors[::50],"ro",label="errors",linestyle='dashed',linewidth=1,markersize=7)
pl.semilogy(k[::50],Error_[::50],"go",label="fit1",linestyle='dashed',linewidth=1,markersize=6)
pl.semilogy(k[::50],Error[::50],"bo",label="fit2",linestyle='dashed',linewidth=1,markersize=4)
pl.title("Errors(Semilog)")
pl.xlabel("$k$ (number of iterations)")
pl.ylabel("Error")
pl.legend()
pl.grid(True)
pl.show()

#Plotting the actual error vector and the error vectors calculated by the two fits on loglog
#We are taking every 50th point in the vector.
fig2 = pl.figure(2)
pl.loglog(k[::50],errors[::50],"ro",label="errors",linestyle='dashed',linewidth=1,markersize=7)
pl.loglog(k[::50],Error_[::50],"go",label="fit1",linestyle='dashed',linewidth=1,markersize=6)
pl.loglog(k[::50],Error[::50],"bo",label="fit2",linestyle='dashed',linewidth=1,markersize=4)
pl.title("Errors(loglog)")
pl.xlabel("$k$ (number of iterations)")
pl.ylabel("Error")
pl.legend()
pl.grid(True)
pl.show()

#Plotting the 3_D surface plot of potential
fig3 = pl.figure(3)
ax=p3.Axes3D(fig3)
pl.title("The 3-D surface plot of the potential")
surf = ax.plot_surface(X,Y, phi, rstride=1, cstride=1, cmap=pl.cm.jet,linewidth=1)
pl.xlabel("$x(cm)$")
pl.ylabel("$y(cm)$")
pl.show()

#Plotting the contour plot of potential after solving the Laplace equation
fig4 = pl.figure(4)
pl.contourf(X,Y,phi)    
pl.title("Contour Plot of Potential(2D) after solving")
pl.scatter(X[ii],Y[ii],color="red",label="Electrode Nodes")
pl.xlabel("X($cm$)")
pl.ylabel("Y($cm$)")
pl.legend()
pl.colorbar()
pl.show()

#Arrays to store the x and y component of currents
Jx = np.zeros((Nx,Ny))
Jy = np.zeros((Nx,Ny))

#Calculating vector current density components
Jx = -0.5*(phi[1:-1,:-2] - phi[1:-1,2:])
Jy = -0.5*(phi[:-2,1:-1] - phi[2:,1:-1])

#Plotting the vector Plot of Currents
fig5 = pl.figure(5)
pl.quiver(X[1:-1,1:-1],Y[1:-1,1:-1],Jx,Jy)
pl.scatter(X[ii],Y[ii],color="red")
pl.title("The vector plot of the current flow")
pl.xlabel("X($cm$)")
pl.ylabel("Y($cm$)")
pl.show()

NetError = net_error(A,B)                 #calling the net_error() to find the net errors for the estimated A and B for a range of Niter

#Plotting the net error vs no. of iterations.
fig6 = pl.figure(6)
pl.semilogy(iter_,NetError,'ro',linestyle='dashed',linewidth=1,label='Net Error')
pl.title("Net Error vs Number of iterations")
pl.xlabel("Niter")
pl.ylabel("Net errror")
pl.legend()
pl.grid(True)
pl.show()
