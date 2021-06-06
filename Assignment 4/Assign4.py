"""
Name       : Aman Kumar
Assignment : 4
Date       : 10-03-2021
Inputs     : Nothing            
Output     : i) Plot of exp(x), cos(cos(x)) along  with  the expected fourier apprixamation and approximation through least squares.
            ii) Plot the magnitude of coefficients for both the functions on semilogy and loglog found through both methods. Euler's formulae and Least sqaure best fit
           iii) The largest absolute difference between the two sets of coefficients.
"""

#Importing modules that are required
from math import cos,sin,exp
import numpy as np                                              #For arrays and some mathematical functions and constants
from scipy.integrate import quad                                #For integration
import pylab as pl                                              #For plotting

#Defining the exp(x) function. It can take vector as input and return a vector as output
def f1(x):
    return(np.exp(x))

#Defining the exp(x) function. It can take vector as input and return a vector as output
def f2(x):
    return(np.cos(np.cos(x)))

#Defining the two functions required in the integration method to find Fourier coefficients
def u(x,f,k):
    return(f(x)*cos(k*x))
def v(x,f,k):
    return(f(x)*sin(k*x))

"""
Function to Calculate the fisrt 51 fourier coefficients of the function f(x) by integration.
It uses Euler's formulae to do so.
"""
def cal_coeff(f,coeffs):
    coeffs[0] += (1/(2*Pi))*quad(f,0,2*Pi)[0]                     #Calculating the value of a0
    
    for i in range(1,26):                                         #For calculating the coefficients a1,b1,....,a25,b25
        coeffs[2*i - 1] += (quad(u,0,2*Pi,args=(f,i))[0])/Pi      #Integrating using quad()
        coeffs[2*i] += (quad(v,0,2*Pi,args=(f,i))[0])/Pi

"""
Function to Calculate the fisrt 51 fourier coefficients of the function f(x) by Least squares best fit approach.
"""
def cal_coeff_lsq(A,f):
    if f == f1:
        b = f1(x_)                             #x_ is an array from 0 to 2pi in 400 steps
    elif f == f2:
        b = f2(x_)
    return(pl.lstsq(A,b,rcond=None)[0])        #Finding coefficients using lstsq()

"""
This function has these roles- i) Plot the actual function in [-2pi,4pi)
                              ii) PLot the expected plot from fourier series
                             iii) PLot the approximation got by least squares approach 
"""    
def Plot_fn(f):
    y1 = f(x)                         #f(x) can operate with vectors. y = f(x) ; x in [-2pi,4pi)
    y3 = f(x_)                        #y = f(x) ; x in [0,2pi)
    y3 = np.concatenate((y3,y3,y3))
    if f == f1:                       #If function is exp(x)
        Title = "$e^x$ on semilog"
        y2 = np.dot(A,coeffs_f1_ls)                                                         #Calculating A.c which should be equal to the function values
        pl.semilogy(x,y1,label="Actual function",color='red')                               #the actual function
        pl.semilogy(x,y3.transpose(),label="Expected",color='black',linestyle='dashed')     #the expected plot from fourier series
        pl.semilogy(x_,y2,'go',label="lstsq approximation")                                 #the approximation got by least squares approach 
    
    elif f == f2:                    #If function is cos(cos(x))
        Title = "$cos(cos(x))$"
        y2 = np.dot(A,coeffs_f2_ls)                                                         #Calculating A.c which should be equal to the function values
        pl.plot(x,y1,label="Actual function",color='red')                                   #the actual function
        pl.plot(x,y3.transpose(),label="Expected",color='black',linestyle='dashed')         #the expected plot from fourier series
        pl.plot(x_,y2,'go',label="lstsq approximation")                                     #the approximation got by least squares approach

    pl.title(Title)
    pl.xlabel("$x$")
    pl.ylabel(Title)
    pl.legend()
    pl.grid(True)
    pl.show()
 
"""
This function plots the semilog plot for magnitude of coefficients obtained by both methods i.e. Integration and Least sqaures 
""" 
def Semilog_Plot(n,f):
    #If function is exp(x)
    if f == f1:
        pl.semilogy(n,abs(coeffs_f1),'ro',label="$Integration$",linestyle='dashed',linewidth=1)           #Plotting coefficients by integration by red circles on semilog
        pl.semilogy(n,abs(coeffs_f1_ls),'go',label="$Least sqaures$",linestyle='dashed',linewidth=1)      #Plotting coefficients by Least squares by green circles on semilog
        pl.title("Plot of Fourier coefficients of $e^x$ on semilog")
    #If function is cos(cos(x))
    elif f == f2:
        pl.semilogy(n,abs(coeffs_f2),'ro',label="$Integration$",linestyle='dashed',linewidth=1)           #Plotting coefficients by integration by red circles on semilog
        pl.semilogy(n,abs(coeffs_f2_ls),'go',label="$Least sqaures$",linestyle='dashed',linewidth=1)      #Plotting coefficients by Least squares by green circles on semilog
        pl.title("Plot of Fourier coefficients of $cos(cos(x))$ on semilog")
    pl.xlabel("$n$")
    pl.ylabel("|$coeff$|")
    pl.grid(True)
    pl.legend()     
    pl.show()

"""
This function plots the semilog plot for magnitude of coefficients obtained by both methods i.e. Integration and Least sqaures 
"""
def LogLog_Plot(n,f):
    if f == f1:
        pl.loglog(n,abs(coeffs_f1),'ro',label="$Integration$",linestyle='dashed',linewidth=1)            #Plotting coefficients by integration by red circles on loglog
        pl.loglog(n,abs(coeffs_f1_ls),'go',label="$Least sqaures$",linestyle='dashed',linewidth=1)       #Plotting coefficients by Least squares by green circles on loglog
        pl.title("Plot of Fourier coefficients of $e^x$ on loglog")
    elif f == f2:
        pl.loglog(n,abs(coeffs_f2),'ro',label="$Integration$",linestyle='dashed',linewidth=1)            #Plotting coefficients by integration by red circles on loglog
        pl.loglog(n,abs(coeffs_f2_ls),'go',label="$Least sqaures$",linestyle='dashed',linewidth=1)       #Plotting coefficients by Least squares by green circles on loglog
        pl.title("Plot of Fourier coefficients of $cos(cos(x))$ on loglog")
    pl.xlabel("$n$")
    pl.ylabel("|$coeff$|")
    pl.grid(True)
    pl.legend()     
    pl.show()

"""
i)This function compares the two sets of coefficients
ii)Finds the largest absolute difference between the two sets of coefficients
"""
def Compare():
    return(max(abs(coeffs_f1 - coeffs_f1_ls)),max(abs(coeffs_f2 - coeffs_f2_ls)))


Pi = np.pi                                     #Defining pi for future use
    

x = pl.linspace(-2*Pi,4*Pi,1201)[:-1]          #Defining array x = [-2pi,4pi) in 1200 steps
x_ = x[400:800]                                #Defining array x_ = 0,2pi) in 400 steps

n = np.array(range(51))                        #Array for indexing the 51 coefficients       
coeffs_f1 = np.zeros(51)                       #Fourier coefficients of exp(x) through integration
coeffs_f2 = np.zeros(51)                       #Fourier coefficients of exp(x) through least sqaures
coeffs_f1_ls = np.zeros(51)                    #Fourier coefficients of cos(cos(x)) through integration
coeffs_f2_ls = np.zeros(51)                    #Fourier coefficients of cos(cos(x)) through least sqaures


#Creating the A matrix
A = np.zeros((400,51))                         #For storing the A matrix
A[:,0] = 1
for i in range(1,26):
    A[:,2*i - 1] = np.cos(i*x_)
    A[:,2*i] = np.sin(i*x_)

"""
Now just calling different functions in the desired order
"""
cal_coeff(f1,coeffs_f1)                        #calculating and storing fourier coefficients of exp(x) through integration
cal_coeff(f2,coeffs_f2)                        #calculating and storing fourier coefficients of exp(x) through least sqaures
coeffs_f1_ls=cal_coeff_lsq(A,f1)               #calculating and storing fourier coefficients of cos(cos(x)) through integration
coeffs_f2_ls=cal_coeff_lsq(A,f2)               #calculating and storing fourier coefficients of cos(cos(x)) through least squares
Plot_fn(f1)
Plot_fn(f2)
Semilog_Plot(n,f1)
LogLog_Plot(n,f1)
Semilog_Plot(n,f2)
LogLog_Plot(n,f2)

#Printing the largest absolute difference between the two sets of coefficients for both the functions
max_deviation = Compare()
print("\nMax deviation in the coefficients of exp(x) :",max_deviation[0])
print("\nMax deviation in the coefficients of cos(cos(x)) :",max_deviation[1])       
