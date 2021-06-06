"""
Author     : Aman Kumar
Assignment : 6 : Tubelight Simulation
Date       : 14-04-2021
Inputs     : 1. n(spatial frid size)
             2. M(avg number of electrons injected per turn)
             3. Msig(stddev of number of electrons injected each turn)
             4. nk(number of turns)
             5. u0(threshold velocity)
             6. p(probability of ionization)            
Outputs    : 1. Electron density plot
             2. Population plot of light intensity
             3. Electron phase space
             4. Intensity data table
Important  : 
"""
#Importing important libraries
from sys import argv               #For taking command line arguments
import numpy as np                 #Mainly for working with arrays
import random as rd
import pylab as pl                 #Mainly for plotting

"""
NOTE: If you wish to update any parameter(s), then you have to pass the rest of the parameter(s) too.
      i.e. if the number of command line arguments is not equal to six, then the rogram runs using the default values
"""
if len(argv) != 7:                           #Checking if all 6 parameters have been passed
    n,M,Msig,nk,u0,p = 100,5,2,500,5,0.25    #Default values
    print("Usage: python",argv[0],"n M Msig nk u0 p")
    print("The program will run using default parameter values. If you wish to update any parameter(s), then you have to pass the rest of the parameter(s) too.")
else:
    #Updating the values user has passed
    n = int(argv[1])                #spatial frid size             
    M = int(argv[2])                #avg number of electrons injected per turn
    Msig = float(argv[3])           #stddev of number of electrons injected each turn
    nk = int(argv[4])               #number of turns
    u0 = float(argv[5])             #threshold velocity
    p = float(argv[6])              #probability of ionization

#Creating vectors to hold the electron information
xx = np.zeros(n*M)                  #Electron position
u = np.zeros(n*M)                   #Electron velocity
dx = np.zeros(n*M)                  #Displacement in current turn
#Lists to accumulate information as part of the simulation
I = []                              #Intensity of emitted light
X = []                              #Electron position
V = []                              #Electron velocity

"""
The Loop
-This is the main loop of the program
-It performs the simulation
-Saves the Intensity, Position and Velocity data in I, X, V respectively
"""
ii = np.where(xx > 0)              #Finding indices of existing electrons
for k in range(nk):
    #ii = np.where(xx > 0)
    dx[ii] = u[ii] + 0.5           #Finding displacement for the electrons in this turn
    xx[ii] = xx[ii] + dx[ii]       #Updating the electron position
    u[ii] = u[ii] + 1              #Since acceleration is taken as 1 unit. Thus increasing velocity 
    
    jj = np.where(xx >= n)         #Finding electrons that have reached Anode. They are lost now.
    xx[jj], dx[jj], u[jj] = 0,0,0  #Resetting there position, velocity and displacement
    
    kk = np.where(u >= u0)         #Finding electrons having atleast threshold energy
    ll = np.where(np.random.rand(len(kk[0]))<=p)
    kl = kk[0][ll]                 #Electrons at these indices will suffer collision
    
    u[kl] = 0                      #After inelastic collision they lose all energy
    xx[kl] = xx[kl] - dx[kl]*rd.random()
    I.extend(xx[kl].tolist())      #Light is emitted where collision happens. Thus saving that data in I
    
    m = round(pl.randn()*Msig + M)    #Numner of electrons to be injected
    zz = np.where(xx == 0)         #Finding available space in the array.
    xx[zz[0][:m]] = 1              #Newly injected electrons are at position 1
    dx[zz[0][:m]] = 0              #Newly injected electrons have displacement = 0          
    u[zz[0][:m]] = 0               #Newly injected electrons have velocity = 0
    
    ii = np.where(xx > 0)          #Existing elecrons
    X.extend(xx[ii].tolist())      #Adding there position to X
    V.extend(u[ii].tolist())       #Adding there velocity to V
    
"""
Electron Density Plot
- number of electrons betweeen i and i+1
"""
fig0 = pl.figure(0)
pl.hist(X,n)
pl.title("Population plot for Electron Density")
pl.grid(True)
pl.xlabel("Electron position")
pl.ylabel("Number of electrons")
pl.show()

"""
Light Intensity Plot
"""
fig1 = pl.figure(1)
count,bins,rec=pl.hist(I,n)
pl.title("Population plot for Light Intensity")
pl.grid(True)
pl.xlabel("Position")
pl.show()

"""
Electron phase space
"""
fig2 = pl.figure(2)
pl.scatter(X,V,marker="x")
pl.title("Electron Phase space")
pl.grid(True)
pl.xlabel("x")
pl.ylabel("velocity")
pl.show()

#The following part is for printing the intensity table
xpos = 0.5*(bins[0:-1]+bins[1:])       #Converting bin positions to mid point values
print("\nIntensity data:\n")
print("\txpos\tcount")
ogm=np.c_[xpos, count]                 #Concatenating the xpos and count vectors. column-wise
s1 = str(ogm)
s2 = s1.replace('], [','\n')
s3 = s2.replace('[', '')
s4 = s3.replace(']','')
s5 = s4.replace(', ','\t')
print(s5)
