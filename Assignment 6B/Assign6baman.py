"""
Author     : Aman Kumar
Assignment : 6B : The Laplace Transform
Date       : 24-04-2021
Inputs     : NO INPUTS from the user end
Outputs    : 1. Time response of a spring with different values of decay
             2. Time response of spring with different frequencies of forcing functions
             3. Time evolution of a coupled spring problem
             4. Magnitude and Phase response of an RLC circuit
             5. Output voltage of the RLC circuit when input is given
"""
#Importing necessary modules
import pylab as pl                   #For plotting and maths functions and handling arrays
import scipy.signal as sp            #For using the signal toolbox
"""
This function returns X(s) = F(s)/(s^2 + 2.25) for the spring problem.
Two arguments - 'freq' of the cos function
              - 'decay' of the exponential
"""
def spring_Trnsfr(decay,freq):
    return(sp.lti([1,decay],[1,2*decay,decay**2 + freq**2 + 2.25,4.5*decay,2.25*(decay**2 + freq**2)]))

"""
Q1 : Time response of spring with 
    - decay     = 0.5/s
    - frequency = 1.5 rad/s
"""
X1 = spring_Trnsfr(0.5,1.5)                        #Transfer function with decay = 0.5, freq = 1.5
t,x = sp.impulse(X1,None,pl.linspace(0,50,501))    #Finding the impulse response of X1(s), i.e. x(t)

#Plotting x(t)
pl.figure(0)
pl.plot(t,x,label="$x(t)$")
pl.title("Time response for decay = 0.5 and frequency = 1.5 rad/s")
pl.xlabel("$t$")
pl.ylabel("$x(t)$")
pl.grid(True)
pl.show()

"""
Q2 : Time response of spring with 
    - decay     = 0.05/s (much smaller decay)
    - frequency = 1.5 rad/s
"""
X2 = spring_Trnsfr(0.05,1.5)                      #Transfer function with decay = 0.05, freq = 1.5
t,x = sp.impulse(X2,None,pl.linspace(0,50,501))   #Finding the impulse response of X2(s), i.e. x(t)

#Plotting x(t)
pl.figure(1)
pl.plot(t,x,label="$x(t)$")
pl.title("Time response for decay = 0.05 and frequency = 1.5 rad/s")
pl.xlabel("$t$")
pl.ylabel("$x(t)$")
pl.grid(True)
pl.show()

"""
Q3 : Time response of spring with 
     - decay     = 0.05/s (much smaller decay)
     - frequency = from 1.4 to 1.6 rad/s in steps of 0.05

"""
Freq = pl.arange(1.4,1.65,0.05)             #Frequency vector for using frequencies 1.4 to 1.6 rad/s
H = sp.lti([1],[1,0,2.25])                  #The transfer function 1/(s^2 + 2.25)
t = pl.linspace(0,100,1001)                 #Simulating for 100 s
label_ = []                                 #For making the legend                

pl.figure(2)
pl.title("Time response of spring with different frequency inputs")
pl.xlabel("$t$")
pl.ylabel("$x(t)$")

for fq in Freq:
    f = pl.cos(fq*t)*pl.exp(-0.05*t)*(t>0)   #Input function
    t,x,svec = sp.lsim(H,f,t)
    pl.plot(t,x)                             #Plotting time response on the same plot for all frequencies
    label_.append("f = "+ str(fq))
    
pl.legend(label_)
pl.show()
    
"""
Q4: Coupled Spring Oscillation
"""
X = sp.lti([1,0,2],[1,0,3,0])                     #X(s) = (s^2 + 2)/(s^3 + 3s)
Y = sp.lti([2],[1,0,3,0])                         #Y(s) = 2/(s^3 + 3s)

t,x = sp.impulse(X,None,pl.linspace(0,20,201))    #Finding x(t)
t,y = sp.impulse(Y,None,pl.linspace(0,20,201))    #Finding y(t)

#Plotting x(t) and y(t) on the same plot
pl.figure(3)
pl.title("Coupled Spring Oscillations")
pl.xlabel("$t$")
pl.plot(t,x,label = "$x(t)$")
pl.plot(t,y,label = "$y(t)$")
pl.legend()
pl.grid(True)
pl.show()

"""
Q5: Transfer function of given RLC circuit
    - Magnitude response
    - Phase response
    
    Tranfer function is H(s) = 1/((LC)s^2 + (RC)s + 1)
"""
H = sp.lti([1],[1e-12,1e-4,1])          #Defining the system transfer function
w,S,phi = H.bode()

pl.figure(4)
pl.subplot(2,1,1)                       #First subplot is for Magnitude response
pl.title("Magnitude response")
pl.xlabel("$w$")
pl.ylabel("|H(jw)| (dB)")
pl.semilogx(w,S)
pl.grid(True)

pl.subplot(2,1,2)                       #Second subplot is for Phase response
pl.title("Phase Response")
pl.semilogx(w,phi)
pl.xlabel("$w$")
pl.ylabel("phase(H(jw)) (degrees)")
pl.semilogx(w,phi)
pl.grid(True)
pl.show()

"""
Q6: Finding output voltage when input voltage is given
    vi(t) = cos(1e3t)u(t) - cos(1e6t)u(t)
    
    Tranfer function is H(s) = 1/((LC)s^2 + (RC)s + 1)
"""
t = pl.arange(0,0.01,1e-7)                   #time vector from 0 to 10ms
Vin = (pl.cos(1e3*t) - pl.cos(1e6*t))*(t>0)  #Input voltage vector
t,Vout,svec = sp.lsim(H,Vin,t)               #Finding the output voltage vector

#Plotting output voltage from 0 to 10ms
pl.figure(5)
pl.title("RLC output till 10 ms")
pl.plot(t,Vout)
pl.xlabel("$t$")
pl.ylabel("$Vout$")
pl.grid(True)
pl.show()

#Plotting output voltage from 0 to 30us
pl.figure(6)
pl.title("RLC output till 30 us")
pl.plot(t[:301],Vout[:301])
pl.xlabel("$t$")
pl.ylabel("$Vout$")
pl.grid(True)
pl.show()
