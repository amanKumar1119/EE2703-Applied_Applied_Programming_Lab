"""
Author     : Aman Kumar
Assignment : 9 : Spectra of non-periodic signals
Date       : 25-05-2021
Inputs     : NO INPUTS from the user end.
Outputs    : 1. Spectrum of sin(sqrt(2)t) without windowing.
             2. Spectrum of sin(sqrt(2)t) with windowing.
             3. Spectrum of (cos(0.86t))^3 without windowing.
             4. Spectrum of (cos(0.86t))^3 with windowing.
             5. Extracted spectrum from a 128 element vector known to contain cos(w0*t + delta).
             6. Extracted spectrum from a 128 element vector known to contain cos(w0*t + delta) with added noise.
             7. Estimated value of w0 and delta in both the cases.
             8. Surface plot to show how the frequency of the signal varies with time.
"""
#Importing necessary libraries
import pylab as p
from pylab import pi                #Value of pi is used a lot in this code

"""
The function to plot the spectrum for different functions. Its arguments:
    1. fmax : 1/dt = 1/(t[1] - t[0])
    2. y : function
    3. Title : title of the plot
    4. fig_no : number of the figure
    5. Xlim : x-axis range in the plot
    6. wind : True if windowing is done, False if not done. (Default = False)
    7. Xticks : ticks along x-axis. (Default = None)
    8. Yticks : ticks along y-axis. (Default = None)

Returns : 1. w : the frequency axis(vector)
          2. Y : calculated transform
"""
def Spectrum(fmax,y,Title,fig_no,Xlim,wind=False,Xticks=None,Yticks=None):
    
    N = len(y)                        #Number of samples
    if wind:                          #Checking if windowing is to be done
        n = p.arange(N)
        wnd = p.fftshift(0.54 + 0.46*p.cos(2*pi*n/(N-1)))  #The Hamming window
        y = y*wnd                     #Multiplying the function to window in time domain
        
    y[0] = 0                                    #the sample corresponding to -tmax should be set zero
    y = p.fftshift(y)
    Y = p.fftshift(p.fft(y))/N                  #Finding the Transform
    w = p.linspace(-pi*fmax,pi*fmax,N+1)[:-1]   #Frequency vector

    p.figure(fig_no)
    p.subplot(2,1,1)                            #Magnitude spectrum
    p.title(Title)
    p.plot(w,abs(Y),'bo',linestyle = "dashed",lw = 1,markersize = 3)
    p.xlim(Xlim)
    p.yticks(Yticks)
    p.xticks(Xticks)
    p.ylabel(r"|$Y$|")
    p.grid(True)
    
    p.subplot(2,1,2)                                #Phase spectrum
    p.plot(w,p.angle(Y)*180/pi,'ro',markersize = 3) #Plotting phase in degrees
    p.yticks(p.arange(-180,181,90))                 #Plotting phase in degrees
    p.xticks(Xticks)
    p.xlim(Xlim)
    p.ylabel(r"Phase of $Y$")
    p.xlabel(r"$\omega$")
    p.grid(True)
    p.savefig("Figure "+str(fig_no)+".png")  #Saving the figure
    p.show()
    
    return(w,Y)

"""
Function to estimate the values of "w0" and "delta" from the given spectrum.
-- The peak will not be visible clearly because of the fact that resolution of the frequecny axis is not enough.
-- To obtain w0 by we take a weighted average of all the w weighted with the magnitude of the DFT.  
-- delta can be found by calculating the phase of the discrete fourier transform at w0 nearest to estimated w.

Arguments : 1. w : frequecny axis for the transform Y.
            2. Y : transform of y
            3. prnt : Just for some formatting in printing the result. (Default = "")
"""
def w0_delta(w,Y,prnt=""):
    ii = p.where(w > 0)                                       #Indexes of all w>0
    w_estimate = sum(w[ii]*abs(Y[ii])**2)/sum(abs(Y[ii])**2)  #Taking weighted average of all w>0 with magnitude of DFT as weights
    i = abs(w - w_estimate).argmin()                          #Finding index of nearest w to the estimated w. This is done for finding delta
    delta_estimate = p.angle(Y[i])                            #delta(estimated) = angle of Y at the index found above.
    
    print("\nEstimated w0"+prnt+" = ",w_estimate)             #Printing the estimated w
    print("Estimated delta"+prnt+" = ",delta_estimate)        #Printing the estimated delta

#Plotting the spectrum of sin(\sqrt{2}t) without windowing
t = p.linspace(-pi,pi,65)[:-1]                   #64 points from -pi to pi
dt = t[1] - t[0];fmax = 1/dt                     #getting fmax
y = p.sin(p.sqrt(2)*t)                           #The given function
Title = r"Spectrum of $sin(\sqrt{2}t)$"
w,Y = Spectrum(fmax,y,Title,0,[-10,10])          #Calling the function Spectrum to plot its spectrum

#Plotting the spectrum of sin(\sqrt{2}t) with windowing(same number of points i.e. 64)
Title = r"Spectrum of $sin(\sqrt{2}t)w(t)$"
w,Y = Spectrum(fmax,y,Title,1,[-8,8],True,Yticks=p.arange(0,0.26,0.05))

#Plotting the spectrum of sin(\sqrt{2}t) with windowing with 4 times the number of points(256)
t = p.linspace(-4*pi,4*pi,257)[:-1]
dt = t[1] - t[0];fmax = 1/dt
y = p.sin(p.sqrt(2)*t)
Title = r"Spectrum of $sin(\sqrt{2}t)w(t)$ with four times the number of points"
w,Y = Spectrum(fmax,y,Title,2,[-4,4],True,Yticks=p.arange(0,0.26,0.05))

#Spectrum of cos(0.86t)^3 without Hamming window
#t is still the same as above i.e. p.linspace(-4*pi,4*pi,257)[:-1]
y = p.cos(0.86*t)**3
Title = r"Spectrum of $cos^3(\omega_0 t)$"
w,Y = Spectrum(fmax,y,Title,3,[-5,5],Xticks=p.arange(-5,6,1),Yticks = p.arange(0,0.3,0.05))

#Spectrum of cos(0.86t)^3 with Hamming window
Title = r"Spectrum of $cos^3(\omega_0 t)w(t)$"
w,Y = Spectrum(fmax,y,Title,4,[-5,5],True,Xticks=p.arange(-5,6,1))

#Extracting the spectrum of cos(w0t + delta) without noise
w0,delta = 1.45,0.5                #Arbitrary values for w0 and delta
t = p.linspace(-pi,pi,129)[:-1]    #Creating 128 element time axis as the given vector is 128 elemts
dt = t[1] - t[0];fmax = 1/dt
y = p.cos(w0*t + delta)            #Creating the 128 element vector
Title = r"Extracted spectrum of $cos(w_0 t + \delta)$ for $w_0$ = " + str(w0) + " and $\delta$ = " + str(delta)

#Calling the function Spectrum to : 1. Extract and plot the spectrum of the given 128 element vector
#                                   2. Get w and Y, which ae used as arguments in the "w0_delta()" function to estimate w0 and delta
w,Y = Spectrum(fmax,y,Title,5,[-6,6],True,Xticks=p.arange(-6,7,1),Yticks = p.arange(0,0.26,0.05))

#Estimating w0 and delta
w0_delta(w,Y)

#Extracting the spectrum of cos(w0t + delta) with noise
y = p.cos(w0*t + delta) + 0.1*p.randn(128)          #Adding noise to the previous vector
Title = r"Extracted spectrum of noisy $cos(w_0 t + \delta)$ for $w_0$ = " + str(w0) + " and $\delta$ = " + str(delta)
w,Y = Spectrum(fmax,y,Title,6,[-6,6],True,Xticks=p.arange(-6,7,1),Yticks = p.arange(0,0.26,0.05))

#Estimating w0 and delta
w0_delta(w,Y," with noise")

#Spectrum of "Chirped" signal
t = p.linspace(-pi,pi,1025)[:-1]                             #time axis : 1024 points between [-pi,pi)
dt = t[1] - t[0];fmax = 1/dt
y = p.cos(16*(1.5 + t/(2*pi))*t)
Title = r"Spectrum of $cos(16(1.5 + \frac{t}{2\pi})t)w(t)$"
w,Y = Spectrum(fmax,y,Title,7,[-50,50],True,Xticks = p.arange(-50,51,10))

"""
The following code is for making the surface plot
Here, t_array, y_array, Y_array are all arrays of size 16x64
"""
t_array = p.array(p.array_split(t,16))                #Dividing the t array into 16 sections of 64 elements each
y_array = p.cos(16*(1.5 + t_array/(2*pi))*t_array)    #Calculating and storing the function values at those values of t

n = p.arange(64)
wnd = p.fftshift(0.54 + 0.46*p.cos(2*pi*n/63))
y_array = y_array*wnd                                 #Multiplying all 16 sections of y with window function
y_array[:,0] = 0                                      #the sample corresponding to -tmax should be set zero in all 16 sections
Y_array = p.fftshift(p.fft(y_array))/64               #Calculating the transform

t = t[::64]
w = p.linspace(-pi*fmax,pi*fmax,65)[:-1]
t,w = p.meshgrid(t,w)

#Plotting the surface plot
fig8 = p.figure(8)
ax = fig8.add_subplot(111,projection = '3d')
surf=ax.plot_surface(w,t,abs(Y_array[::-1]).T,cmap='viridis',linewidth=0, antialiased=False)
fig8.colorbar(surf,shrink = 0.5,aspect = 5)
ax.set_title(r"Surface Plot")
p.ylabel(r"$\omega \rightarrow$")
p.xlabel(r"$t \rightarrow$")
p.savefig("Figure 8.png")  #Saving the figure
p.show()
