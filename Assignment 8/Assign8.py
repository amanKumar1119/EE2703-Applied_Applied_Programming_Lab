"""
Author     : Aman Kumar
Assignment : 8 : The Digital Fourier Transform
Date       : 18-05-2021
Inputs     : NO INPUTS from the user end.
Outputs    : 1. Spectrum of sin(5t).
             2. Spectrum of (1+0.1cos(t))cos(10t).
             3. Spectrum of (sin(t))^3.
             4. Spectrum of (cos(t))^3.
             5. Spectrum of cos(20t +5cos(t)) : FM signal.
             6. Spectrum of exp(-0.5t^2)
NOTE       : Plotting phase only when magnitude is greater than 1e-3 
"""
#Importing necessary libraries
import pylab as p

"""
The function to plot the spectrum for different functions. Its arguments:
    1. y : function
    2. Nsamples : number of samples
    3. Title : title of the plot
    4. n_fig : number of the figure
    5. Xlim : x-axis range in the plot
    6. tick_size : size of font in ticks
    7. x_ticks : ticks along x-axis
    8. y_ticks : ticks along y-axis
"""
def plot_spectrum(y,Nsamples,Title,n_fig,Xlim,tick_size,x_ticks=None,y_ticks=None):
    Y = p.fftshift(p.fft(y))/Nsamples       #Calculating the tranform
    w = p.linspace(-64,64,Nsamples+1)       #The frequency axis of the plot
    w = w[:-1]

    p.figure(n_fig - 1)
    p.subplot(2,1,1)                        #First subplot : Magnitude
    p.plot(w,abs(Y))
    p.xlim(Xlim)
    p.yticks(y_ticks,size=tick_size)
    p.xticks(x_ticks,size=tick_size)
    p.ylabel(r"$|Y|$",size=11)
    p.title(Title)
    p.grid(True)

    p.subplot(2,1,2)                        #Second subplot : Phase
    ii = p.where(abs(Y) > 1e-3)             #Finding indexes where |Y| > 1e-3
    p.plot(w[ii],p.angle(Y[ii])*(180/p.pi),'ro',markersize=4)
    p.xlim(Xlim)
    p.xticks(x_ticks,size=tick_size)
    p.yticks(p.arange(-180,185,90),size=10)
    p.ylabel(r"Phase of $Y$",size=11)
    p.xlabel(r"$k$",size=11)
    p.grid(True)
#    p.savefig("Figure "+str(n_fig)+".png")  #Saving the figure
    p.show()

#The expected spectrum, of the given gaussean function
def expected_gauss(w):
    return(p.exp(-0.5*w**2)/p.sqrt(2*p.pi))

#The given Gauss function
def Gauss(x):
    return(p.exp(-0.5*x**2))

"""
This function is to find the time range and corresponding number of samples which helps us to get the spectrum of the given Gaussian function accurate upto 6 digits.Its argument :
    1. tolerance - the lower limit of accuracy we want. In out case
                   it is 1e-6

After finding the appropriate T and N, it plots the spectrum of the given gaussian function allong with its expected spectrum.

Returns : T, N, mean error
"""
def best_T_N(tolerance):
    T = 2*p.pi                       #Starting value of T is 2pi
    N = 128                          #Starting value of N is 128 = 2^7
    err = tolerance+1                #Intially making error > tolerance
    
    #This loop will stop only when the error becomes less than tolerance. The value of T and N, when the loop stops will be the desired values
    while True:
        x = p.linspace(-T/2,T/2,N+1)[:-1]           #x range
        w = p.linspace(-64,64,N+1)[:-1]             #Frequency axis of the plot
        y = Gauss(x)                                #The given Gauss function
        Y = p.fftshift(p.fft(y))*T/(2*p.pi*N)       #Calculating the Transform for the current T and N
        Yexp = expected_gauss(w)                    #Expected transform
        err = p.mean(abs(abs(Y) - Yexp))            #Finding the mean error between calculated and expected transforms
        
        #If mean error is less than the given tolerance then break the loop
        if(err < tolerance):
            break
        T = 2*T                                     #Updating T
        N = 2*N                                     #Updating N
    
    #Plotting the spectrum for the T and N that we got
    p.figure(7)
    p.subplot(2,1,1)                                #Subplot 1 : Magnitude
    p.title(r"Spectrum of $exp(-x^2/2)$")
    p.plot(w,abs(Y),label="Calculated Y",color="gold",lw=2)                  #Plotting the calculated |Y|
    p.plot(w,Yexp,label="Expected Y",lw=1,linestyle="dashed",color="black")  #Plotting the expected |Y|
    p.ylabel(r"$|Y|$")
    p.legend()
    p.grid(True)
    p.xlim([-10,10])
    
    #Subplot 2 : Phase.
    #NOTE: I am plotting phase only when magnitude is greater than 1e-3
    p.subplot(2,1,2)
    ii = p.where(abs(Y) > 1e-3)             #Finding indexes where |Y| > 1e-3
    p.plot(w[ii],p.angle(Y[ii])*(180/p.pi),'ro',markersize=4)
    p.xlabel(r"$k$")
    p.ylabel(r"Phase of $Y$")
    p.yticks(p.arange(-180,185,90),size=10)
    p.xlim([-10,10])
    p.grid(True)
#    p.savefig("Figure 8.png")
    p.show()
    return(T,N,err)

"""
First attempt to get the transform of sin(5t)
- not using fftshift
- 2pi point is repeating
- power is not zero for frequencies other than peak
- phase is nearly correct but not exact
"""
#Example 1 sin(5t) "Bad"
x = p.linspace(0,2*p.pi,128)           #x-range fron 0 to 2pi
y = p.sin(5*x)
Y = p.fft(y)                           #Calculating the transform of y

#Plotting the magnitude and phase spectrum
p.figure(0)
p.subplot(2,1,1)                       #Subplot 1 : Magnitude
p.plot(abs(Y))
p.xticks(p.arange(0,130,5),size=5)
p.ylabel(r"$|Y|$",size=11)
p.title(r"Spectrum of $\sin(5t)$")
p.grid(True)

p.subplot(2,1,2)                       #Subplot 2 : Phase
p.plot(p.angle(Y)*(180/p.pi))          #I am plotting the phase in degrees
p.xticks(p.arange(0,130,5),size=5)
p.yticks(p.arange(-180,185,90),size=10)
p.ylabel(r"Phase of $Y$",size=11)
p.xlabel(r"$k$",size=11)
p.grid(True)
#p.savefig("Figure 1.png")
p.show()

"""
Second attempt to get the transform of sin(5t)
- using fftshift
- 2pi point is not repeating
- power is below 1e-15 for frequencies other than peaks
- phase is correct
"""
#Example 2: sin(5t) "Better"
x = p.linspace(0,2*p.pi,129)      #129 samples from 0 to 2pi
x = x[:-1]                        #Dropping the last sample to make it 128(2^7)
y = p.sin(5*x)                    #sampling freq = 128/2pi
Title = "Spectrum of $\sin(5t)$"
plot_spectrum(y,128,Title,2,[-10,10],10,p.arange(-10,11,5),p.arange(0,0.51,0.25))

"""
First attempt to get the transform of (1+0.1cos(t))cos(10t)
- Three peaks not visible separately due to less number of points on the frequency axis
- Only a broad single peak is visible in place of three different peaks
- However, phase is correct
"""
#Example 3: (1+0.1cos(t))cos(10t) "Bad"
y = (1+0.1*p.cos(x))*p.cos(10*x) 
Title = "Spectrum of $(1+0.1cos(t))cos(10t)$"
plot_spectrum(y,128,Title,3,[-15,15],10,p.arange(-15,16,5),p.arange(0,0.51,0.1))

"""
Second attempt to get the transform of (1+0.1cos(t))cos(10t)
- This time we are stretcing the x axis, but keeping the sampling frequency same
- This will give us a tighter spacing between frequency samples
"""
#Example 4: (1+0.1cos(t))cos(10t) "Better"
x = p.linspace(-4*p.pi,4*p.pi,513)  #513 samples from -4pi to 4pi
x = x[:-1]                          #Dropping the last sample to make it 512(2^9)
y = (1+0.1*p.cos(x))*p.cos(10*x)
plot_spectrum(y,512,Title,4,[-15,15],8,p.arange(-15,16,5),p.arange(0,0.51,0.1))

"""
Spectrum of (sin(t))^3
- We are using the same x-axis: 0 to 8pi in 512 steps
                                        or
                               -4pi to 4pi in 512 steps
"""
y = (p.sin(x))**3          #Defining the function
Title = "Spectrum of $sin^3(t)$"
plot_spectrum(y,512,Title,5,[-5,5],10,p.arange(-4,5,1),p.arange(0,0.51,0.1))

"""
Spectrum of (cos(t))^3
- We are using the same x-axis: 0 to 8pi in 512 steps
                                        or
                               -4pi to 4pi in 512 steps
"""
y = (p.cos(x))**3          #Defining the function
Title = "Spectrum of $cos^3(t)$"
plot_spectrum(y,512,Title,6,[-5,5],10,p.arange(-4,5,1),p.arange(0,0.51,0.1))

"""
Spectrum of cos(20t +5cos(t)) : FM signal
- We are using the same x-axis: 0 to 8pi in 512 steps
                                        or
                               -4pi to 4pi in 512 steps
- Plotting phase only when the magnitude is greater than 1e-3
"""
y = p.cos(20*x + 5*p.cos(x))
Title = "Spectrum of $cos(20t +5cos(t))$"
plot_spectrum(y,512,Title,7,[-35,35],8,p.arange(-35,36,5))

"""
Calling the function best_T_N() with a tolerance value of 1e-6. It will find a time range T and corresponding N that gives us a spectrum accurate upto 6 digits.
It will also plot the spectrum.
"""
T,N,error = best_T_N(1e-6)
#Printing T, N and error
print("Best time range : ",T/p.pi,"π",sep = "")
print("Corresponding N :",N,"samples")
print("Mean error :",error)
