"""
Name       : Aman Kumar
Assignment : 3
Date       : 05-03-2021
Inputs     : i) A file containing nine sets of data and time. "fitting.dat"            
Output     : i) Plot of data to be fitted to theory and true value.
            ii) Error bars for first set of data along with true value plot
           iii) Contour plot for mse between between first column of data and assummed model.
            iv) Plot of the error in the estimate of A and B(parameters) for different data files versus the noise in linear scale.
             v) Plot of the error in the estimate of A and B(parameters) for different data files versus the noise in loglog scale.
Description: This code takes as input(by itself) and tries to fit that data to theory by the method of least squares.
"""

#Importing modules that are required
import numpy as np
import pylab as pl
import scipy.special as sp

A0B0 = np.array([1.05,-0.105])                           #Array of actual values of parameters

#Fitting function(Assumed Model)
def g(t,A,B):
    return(A*sp.jn(2,t) + B*t)

#Function to estimate and return the parameters A and B
def estimate_A_B(M,col):
    AB = pl.lstsq(M,col,rcond=None)
    return(AB[0][0],AB[0][1])
    

data = np.loadtxt("fitting.dat")                        #Loading data from "fitting.dat" into array "data"
t = data[:,0]                                           #Extracting time column and 

y0 = g(t,A0B0[0],A0B0[1])                               #True Value calculated by using actual values of parameters and assummed model
stdev = np.logspace(-1, -3, 9)                          #Std dev for the data columns in order


"""
Plot 1: It contains - Plot of true value
                    - Plot of 9 sets of noisy data
"""
pl.figure(0)
for i in range(1,10):
    pl.plot(t,data[:,i],label="\u03C3 = %0.4f" % stdev[i-1])
pl.plot(t,y0,label="True Value",color='black',linewidth = 3)
pl.title("Q3. True Value along with nine other noisy plots")
pl.xlabel("$t$",size = 11)
pl.ylabel("$f(t) + n$",size = 11)
pl.grid(True)
pl.legend()

"""
Plot 2: It contains - Data points of firt column with errorbars
                    - Plot of true value
"""
pl.figure(1)
pl.errorbar(t[::5],data[:,1][::5],stdev[1],fmt='ro',label="error bar")
pl.plot(t,y0,label = "True value",color = 'black')
pl.xlabel("$t$")
pl.title("Q5. Plot of First column of data with error bars and the True value")
pl.grid(True)
pl.legend()

#Constructing the Matrix M asked in Q6
Jt = sp.jn(2,t)
M = pl.c_[Jt,t]
if (np.array_equal(np.dot(M,A0B0),y0)):                     #Verifying whether M.[A0,B0] is equal to the g(t,A0,B0)
    print("M*[A0;B0] is equal to g(t,A0,B0). Verified!")
else:
    print("M*[A0;B0] is NOT equal to g(t,A0,B0).")

"""
Mean Squared Error for column 1 and assummed model for - A ranging from 0 to 2 in steps of 0.1
                                                       - B ranging from -0.2 to 0 in steps of 0.01
"""
A = np.linspace(0, 2, 21)                  #A from 0 to 2 in steps of 0.1
B = np.linspace(-0.2, 0, 21)               #B from -0.2 to 0 in steps of 0.01
a,b = np.meshgrid(A,B)                     #meshgrid for plotting contour
Err = np.zeros((21,21))                    #Matrix to store to store Mean Squared Errors for different combinations of A and B
f1 = data[:,1]                             #First column of data
for i in range(21):
    for j in range(21):
        Err[i,j] += np.sum(((f1 - g(t,A[i],B[j]))**2))/101

"""
Plot 3: Contour PLot of “mean squared error” between the first column of data and the assumed model.
"""
fig=pl.figure(2)
cp = pl.contour(a,b,Err,[0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.225,0.25,0.275,0.3])
#pl.contour(1.05,-0.105,0)
pl.clabel(cp,[0.025,0.05,0.075,0.1],inline=1)                #Labeling in line
fig.colorbar(cp)                                             #Adding a color bar to the plot to indicate the level of contours
pl.title("Q8. Contour plot of error $\epsilon_{ij}$")
pl.xlabel("$A$")
pl.ylabel("$B$")
pl.show()


Aerr,Berr = np.zeros(9),np.zeros(9)                          #Arrays to store the MS error in the prediction of A and B for different amount of noise
for i in range(1,10):
    A_est,B_est = estimate_A_B(M,data[:,i])                  #the function "estimate_A_B()" estimates by the method of least squares
    Aerr[i-1] += ((A_est - A0B0[0])**2)
    Berr[i-1] += (B_est - A0B0[1])**2
 
"""
Plot 4: i) Variation of MS error in estimation of A vs Noise in linear scale
       ii) Variation of MS error in estimation of B vs Noise in linear scale
"""
pl.figure(3)
pl.plot(stdev,Aerr,marker = "*",label="$A_{err}$",linestyle = 'dashed')
pl.plot(stdev,Berr,marker = "*",label="$B_{err}$",linestyle = 'dashed')
pl.grid(True)
pl.xlabel("\u03C3",size=11)
pl.ylabel("$MSerror$")
pl.title("Q10. Variation of Error with Noise(linear scale)")
pl.legend()
pl.show()
    

"""
Plot 4: i) Variation of MS error in estimation of A vs Noise in loglog scale
       ii) Variation of MS error in estimation of B vs Noise in loglog scale
"""
pl.figure(4)
pl.loglog(stdev,Aerr,'ro',label="$A_{err}$")
pl.errorbar(stdev,Aerr,pl.std(Aerr),fmt='ro')
pl.loglog(stdev,Berr,'go',label="$B_{err}$")
pl.errorbar(stdev,Berr,pl.std(Berr),fmt='go')
pl.grid(True)
pl.xlabel("\u03C3",size=11)
pl.ylabel("$MSerror$")
pl.title("Q11. Variation of Error with Noise(loglog scale)")
pl.legend()
pl.show()
