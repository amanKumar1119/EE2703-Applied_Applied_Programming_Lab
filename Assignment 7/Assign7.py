"""
Author     : Aman Kumar
Assignment : 7
Date       : 6-05-2021
Inputs     : NO INPUTS from the user end
Outputs    : 1. Magnitude response of HPF and LPF circuitd given
             2. Step response of given LPF and HPF circuits
             3. Response of the circuits to vi(t) = (sin(2000πt) + cos(2e6*πt))u(t) Volts 
             4. Response of HPF circuit to two damped sinusoids:
                i) cos(1e6t)*exp(-3000t)
               ii) cos(100t)*exp(-3000t)
"""
#Importing necessary modules
import sympy as sp           #For symbolic algebra and certain other functions
import pylab as p            #Mainly for plotting and vectors
import scipy.signal as sg    #For using the Signal toolbox
sp.init_session
#%%
s = sp.symbols('s')          #Declaring 's' as a sympy variable

"""
This Function is for solving the Low Pass Filter Circuit
- It creates A and b matrices. Where A*V = b.
- V is the solution matrix
- It returns the matirces A,b,V
"""
def lowpass(r1,r2,c1,c2,g,vi):
    s = sp.symbols('s')
    #Creating the "A" matrix
    A = sp.Matrix([[0,0,1,-1/g],\
                   [-1/(1+s*r2*c2),1,0,0],\
                   [0,-g,g,1],\
                   [-1/r1-1/r2-s*c1,+1/r2,0,+s*c1]])
    #Creating the "b" matrix
    b = sp.Matrix([0,0,0,-vi/r1])
    V = A.inv()*b                 #Solving for V
    return(A,b,V)

"""
This Function is for solving the High Pass Filter Circuit
- It creates A and b matrices. Where A*V = b.
- V is the solution matrix
- It returns the matirces A,b,V
"""
def highpass(r1,r3,c1,c2,g,vi):
    s = sp.symbols('s')
    #Creating the "A" matrix
    A = sp.Matrix([[0,0,1,-1/g],\
                  [-(s*r3*c2)/(1+s*r3*c2),1,0,0],\
                  [0,-g,g,1],\
                  [1/r1+s*(c1+c2),-s*c2,0,-1/r1]])
    #Creating the "b" matrix
    b = sp.Matrix([0,0,0,vi*s*c1])
    V = A.inv()*b                 #Solving for V
    return(A,b,V)

"""
This Function is for plotting the Magnitude response of a given transfer function.
Used in this code to plot the magnitude response of both LPF and HPF for Vi = δ(t)
"""
def Magnitude_response(Vo):
    s = sp.symbols('s')
    f = sp.lambdify(s,Vo,"numpy")
    p.xlabel("$\u03C9$")             #u03C9 is unicode for omega(w)
    p.loglog(w,abs(f(ss)),label="$|Vo(j\u03C9)|$")
    p.legend()
    p.grid(True)
    p.show()
 
"""
Response(): This function is for plotting the response of a given transfer function 
            to a given input.
            Used in this code - to plot the step response of both LPF and HPF.
                              - to plot the response of LPF to the given input signal  
"""
def Response(H,t,Vin):
    
       t,Vo,svec = sg.lsim(H,Vin,t)           #Finding time response of H to Vin(t) 
       p.plot(t,Vo,label="Vout")
       p.xlabel("$t$")
       p.ylabel("$Vo$")
       p.grid(True)
       p.legend()
       p.show()

"""
This function - finds the coefficients of numerator and denominator of a rational expression
              - returns two lists 1. coeffs of numerator 2. coeffs of denominator
"""       
def get_coeffs(expr):
    num,den = expr.as_numer_denom()      #num, den are numerator and denominator polynomials
    return[sp.Poly(num,s).all_coeffs(),sp.Poly(den,s).all_coeffs()]

w = p.logspace(0,8,801)                  #The frequency vector from 1 to 10**8
ss = 1j*w
t = p.arange(0,1e-3,0.0000001)           #time vector. I have taken the step size 1e-7 as
                                         #we are dealing with functions of frequency 1e6.
"""
1. Magnitude response for both - Low Pass Filter
                               - High Pass Filter 
"""
#1. Magnitude Response of the filters with Vi = δ(t)
A1,b1,V1 = lowpass(10000,10000,1e-9,1e-9,1.586,1)
A2,b2,V2 = highpass(10000,10000,1e-9,1e-9,1.586,1)

Vo_LP1 = V1[3].simplify()                #Laplace tranform of Vo(t) for Vi = δ(t). i.e. Impulse response
print("Low Pass Transfer Function:",Vo_LP1,"\n")
Vo_HP1 = V2[3].simplify()
print("High Pass Trasnfer Function:",Vo_HP1)

#Plotting the Magnitude Response of Lowpass filer in Figure 0
p.figure(0)
p.title("Magnitude response of Low Pass Filter")
Magnitude_response(Vo_LP1)

#PLotting the Magnitude Response of Highpass filer in Figure 1
p.figure(1)
p.title("Magnitude response of High Pass Filter")
Magnitude_response(Vo_HP1)

"""
2. Step Response of both - Low Pass Filter
                         - High Pass Filter
"""
Vin1 = p.heaviside(t,1)          #Unit step function

#Calculting the coefficients of numerator and denominator polynomials
#for the transfer function of the Low Pass Filter
n,d = get_coeffs(Vo_LP1)
n_coeff,d_coeff = p.array(n,dtype="float"),p.array(d,dtype="float")
H_LP = sg.lti(n_coeff,d_coeff)          #Defining the transfer fucntion of LPF

#Plotting the Step Response of Lowpass filer in Figure 2
p.figure(2)
p.title("Step Response of the Low Pass Filter")
Response(H_LP,t,Vin1)

#Calculting the coefficients of numerator and denominator polynomials
#for the transfer function of the High Pass Filter
n,d = get_coeffs(Vo_HP1)
n_coeff,d_coeff = p.array(n,dtype="float"),p.array(d,dtype="float")
H_HP = sg.lti(n_coeff,d_coeff)          #Defining the transfer fucntion of HPF

#Plotting the Step Response of Highpass filer in Figure 3
p.figure(3)
p.title("Step Response of the High Pass Filter")
Response(H_HP,t,Vin1)

"""
3.Response of the circuits to the given input(sum of two sinusoids of very different frequencies)
            vi(t) = (sin(2000πt) + cos(2e6*πt))u(t) Volts 
"""
#The given input function - sum of two sinusoids of very different frequencies
Vin2 = (p.sin(2e3*p.pi*t) + p.cos(2e6*p.pi*t))*p.heaviside(t,1)

#Plotting the response of LPF
p.figure(4)
p.title("Response of the Low Pass Filter for the given input")
Response(H_LP,t,Vin2)                   #Plotting for t=0 to t=1ms

#Plotting the response of HPF
p.figure(5)
p.title("Response of the High Pass Filter for the given input")
Response(H_HP,t[:201],Vin2[:201])       #Plotting for t=0 to t=20µs because the
                                        #high frequency componenet has frequency 2e6

"""
4.Response of the HPF circuit to damped sinusoids
i)  High frequency damped sinusoid cos(1e6t)*exp(-3000t)
ii) Low frequency damped sinusoid cos(100t)*exp(-3000t)
"""
damp1 = p.cos(1e6*t)*p.exp(-3000*t)    #High frequency damped sinusoid       
damp2 = p.cos(100*t)*p.exp(-3000*t)    #Low frequency damped sinusoid

p.figure(6)
p.title("Response of the HPF for the high frequency damped sinusoid")
Response(H_HP,t,damp1)
p.figure(7)
p.title("Response of the HPF for the low frequency damped sinusoid")
Response(H_HP,t,damp2)
