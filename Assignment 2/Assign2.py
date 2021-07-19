"""
Name       : Aman Kumar
Assignment : The Spice Program in Python
Date       : 03-03-2021
Inputs     : i) Name of the netlist file as the only command line argument.
            ii) The netlist file.
Output     : i) Value of node volatges(phasors).
            ii) Values of current(phasors) through volatge sources.
Description: This code takes as input(through command line) the name of a netlist file in format described in the assignment pdf.
             And then tries to solve that circuit by first creating the Modified Nodal Analysis(MNA) matrix and then solving it.
             The rest of the explanation is given along with the code :)
Important  : i) The value of phase should be in degrees
            ii) Frequency is in Hertz. i.e. f = w/2pi
"""
from sys import argv              #To take command line arguments
import numpy as np                #To work with arrays
from cmath import rect            #To get the phasor for V and I

"""Checking if correct number of inputs are given by the user
through the command line."""
if len(argv) != 2:
    print("\nUsage : %s <InputFileName>" % argv[0])
    exit()
netlist_name = argv[1]

#Storing important connstants
(START,END,AC) = (".circuit",".end",".ac")
Pi = np.pi            #Storing value of Pi for future use

"""
Defining classes for the different components supported by my program.
The supported components are R,L,C,V,I. the symbols have there usual meaning
"""
#Class for Resistor
class Resistor:

    def __init__(self,n1,n2,value):
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = float(value)

#Class for Independent Voltage Source        
class V_Source:
    
    def __init__(self,n1,n2,value,phase):         #The phase in degrees
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = rect(value,(Pi*phase)/180)     #Converting phase to radians and then using rect() to get the phasor in rectangular coordinates
 
#Class for Independent Current Source 
class I_Source:
    
    def __init__(self,n1,n2,value,phase):
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = rect(value,(Pi*phase)/180)

#Class for Capacitor        
class Capacitor:

    def __init__(self,n1,n2,value):
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = float(value)

    def impedance(self,w):                      #Calculating the impedance of Capacitor at the given frequency
        if w == 0:
            return(float("inf"))                #In DC Z(c) = infinite
        else:
            return(complex(0,-1/(w*self.val)))   

#Class for Inductor        
class Inductor:

    def __init__(self,n1,n2,value):             #Calculating the impedance of Capacitor at the given frequency
        self.n1 = int(n1)
        self.n2 = int(n2)
        self.val = float(value)

    def impedance(self,w):
        return(complex(0,w*self.val))
"""
  i)Checking if filename given is valid.
 ii)Finding the segment containing the the circuit definition
iii)Checking if the file name given is valid.
"""
try:
    fh = open(netlist_name,"r")             #Trying to open the mentioned file with File Handle "fh"
    lines = fh.readlines()
    fh.close()                              #Closing the file handle "fh"
    del(fh,netlist_name)
    (cstart,cend) = (-1,-2)                 #Indexes to identify the segment containing the circuit definition

    for i in range(len(lines)):
        if START == lines[i][:len(START)]:  #Checking if the line is ".circuit"
            cstart = i
        elif END == lines[i][:len(END)]:    #Checking if the line is ".end"
            cend = i
            break
    w = 0
    
    #This block below is for extracting the frequency from the ".ac" line in case it's an AC circuit
    for i in range(cend + 1,len(lines)):
        if AC == lines[i][:len(AC)]:
            line = lines[i].split("#")[0].rstrip().split(" ")
            w = 2*Pi*float(line[-1])       #Calculating w from frequency
            break

    if cstart >= cend or cstart*cend < 0:
        print("\nInvalid Circuit Definition")
        exit()

except IOError:                             #If the file specified is Invalid and could not be opened
    print("\nCould not open the File mentioned.")
    exit()


#Defining dictionaries for all the components supported
Resistors, V_sources, I_sources, Capacitors, Inductors, nodes = {},{},{},{},{},{}
#To identify which nodes are shorted
Shorts = []

"""
  i)This function identifies(from the first letter of its name) which component is described in a single line of the netlist file.
 ii)Then it creates object of that particular component type and appends them in dictionary for that component.
iii)If a component is shorted(in steady state) this function does not create an object
"""    
def Identify(line):

    if line[0][0] == "R":                    #Resistor 
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Resistors[line[0]] = Resistor(nodes[line[1]], nodes[line[2]], line[3])
    elif line[0][0] == "V":                  #Independent Voltage Source
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            if line[3].lower() == "dc":      #Checking if the source is DC
                V_sources[line[0]] = V_Source(nodes[line[1]], nodes[line[2]], float(line[4]), 0.0)
            elif line[3].lower() == "ac":   #Checking if the source is AC
                V_sources[line[0]] = V_Source(nodes[line[1]], nodes[line[2]], float(line[4])/2, float(line[5]))
    elif line[0][0] == "I":                  #Independent Current Source
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            if line[3].lower() == "dc":      #Checking if the source is DC
                I_sources[line[0]] = I_Source(nodes[line[1]], nodes[line[2]], float(line[4]), 0)
            elif line[3].lower() == "ac":    #Checking if the source is DC
                I_sources[line[0]] = I_Source(nodes[line[1]], nodes[line[2]], float(line[4])/2, line[5])
    elif line[0][0] == "C":                  #Capacitor
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Capacitors[line[0]] = Capacitor(nodes[line[1]], nodes[line[2]], line[3])
    elif line[0][0] == "L":                  #Inductor
        if sorted([nodes[line[1]],nodes[line[2]]]) not in Shorts:
            Inductors[line[0]] = Inductor(nodes[line[1]], nodes[line[2]], line[3])

"""
1.This function finds out which nodes are shorted
2.Then it appends those pairs of nodes to the list "Shorts"
3.It also builds the Dictionary "nodes" with keys as their names as given in the netlist file and values them 0,1,2,3...
4.GND node is always numbered 0
5.This function also tries to catch some errors - if some component in the netlist is not supported
                                                - if GND node is not present in the circuit
                                                - if description of a component in a line is invalid(in this casethat component is skipped)
"""
def nodes_and_shorts(w):
    node_index = 1
    for line in lines[cstart+1:cend]:
        line = line.split("#")[0].rstrip().split(" ")
        try:
            if line[0][0] not in ['R','V','I','C','L']:      #if some component in the netlist is not supported
                print("\nThis program currently does not support some of the elements")
                print("that are present in this circuit.Currently only R,L,C,V,I are supported.")
                print("Symbols have their usual meaning")
                exit()
            
            #Numbering nodes, and making the dictionary of nodes
            for index1 in range(1,3):
                if line[index1] not in nodes.keys():
                    if line[index1] == "GND":
                        nodes[line[index1]] = 0
                    else:
                        nodes[line[index1]] = node_index
                        node_index += 1
            if (line[0][0] == "R") and (float(line[3]) == 0):          #if R=0 then it's a short
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
            elif (line[0][0] == "V") and (float(line[4]) == 0):        #if V=0 then it's a short 
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
            elif (line[0][0] == "L") and (w == 0):                     #Inductor is a short in DC(steady state)
                Shorts.append(sorted([nodes[line[1]],nodes[line[2]]]))
        
        except IndexError:                                  #if description of a component in a line is invalid(in this casethat component is skipped)
            continue
        
    if "GND" not in nodes.keys():                           #if GND node is not present in the circuit
        print("\nThe circuit does not have a conducting path to ground. Feed a proper circuit.")
        exit()

"""
1.This function manages the effects of shorts that are present.
2.Basically what it does is if node i and node j are shorted(i<j) then it connects node j to node i for components with one node connected at j.
3.However if a component has one node connected to i(i<j) then nothing is done as nothing is required
"""
def manage_shorts():
    for short in Shorts:
        for R in Resistors.values():
            if R.n1 == short[1]:
                R.n1 = short[0]
            elif R.n2 == short[1]:
                R.n2 = short[0]
        for C in Capacitors.values():
            if C.n1 == short[1]:
                C.n1 = short[0]
            elif C.n2 == short[1]:
                C.n2 = short[0]
        for L in Inductors.values():
            if L.n1 == short[1]:
                L.n1 = short[0]
            elif L.n2 == short[1]:
                L.n2 = short[0]
        for V in V_sources.values():
            if V.n1 == short[1]:
                V.n1 = short[0]
            elif V.n2 == short[1]:
                V.n2 = short[0]
        for I in I_sources.values():
            if I.n1 == short[1]:
                I.n1 = short[0]
            elif I.n2 == short[1]:
                I.n2 = short[0]

"""
This function is for reading the function line by line
"""                
def Read_Ciruit():
    for line in lines[cstart+1:cend]:
        line = line.split("#")[0].rstrip().split(" ")
        if len(line) in [4,5,6]:                #If some invalid line is present
            Identify(line)


"""
1.This function creates the MNA matrix
2.It does this by adding 'stamps' of all the components to the matrix
3.G - Conductance matrix; I - Source matrix
"""
def Create_MNA_matrix():

    for R in Resistors.values():
        r = R.n1
        c = R.n2
        if r == c:
            continue
        elif r == 0:
            G[c-1,c-1] += 1/R.val
        elif c == 0:
            G[r-1,r-1] += 1/R.val
        else:
            G[r-1,r-1] += 1/R.val
            G[r-1,c-1] -= 1/R.val
            G[c-1,r-1] -= 1/R.val
            G[c-1,c-1] += 1/R.val

    for C in Capacitors.values():
        r = C.n1
        c = C.n2
        if r == c:
            continue
        elif r == 0:
            G[c-1,c-1] += 1/C.impedance(w)
        elif c == 0:
            G[r-1,r-1] += 1/C.impedance(w)
        else:
            G[r-1,r-1] += 1/C.impedance(w)
            G[r-1,c-1] -= 1/C.impedance(w)
            G[c-1,r-1] -= 1/C.impedance(w)
            G[c-1,c-1] += 1/C.impedance(w)

    for In in Inductors.values():
        r = In.n1
        c = In.n2
        if r == c:
            continue
        elif r == 0:
            if In.impedance(w) != 0:                      #adding only if impedance is non-zero
                G[c-1,c-1] += 1/In.impedance(w)
        elif c == 0:
            if In.impedance(w) != 0:
                G[r-1,r-1] += 1/In.impedance(w)             
        else:
            if In.impedance(w) != 0:
                G[r-1,r-1] += 1/In.impedance(w)
                G[r-1,c-1] -= 1/In.impedance(w)
                G[c-1,r-1] -= 1/In.impedance(w)
                G[c-1,c-1] += 1/In.impedance(w)               

    aux_index = len(nodes) - 1 - len(Shorts)
    for V in V_sources.values():
        r = V.n1
        c = V.n2
        if r == c:
            continue
        elif c == 0:
            G[r-1,aux_index] += 1
            G[aux_index,r-1] += 1
            I[aux_index] += V.val
            aux_index += 1
        elif r == 0:
            G[c-1,aux_index] -= 1
            G[aux_index,c-1] -= 1
            I[aux_index] += V.val
            aux_index += 1
        else:
            G[r-1,aux_index] += 1
            G[c-1,aux_index] -= 1
            G[aux_index,r-1] += 1
            G[aux_index,c-1] -= 1
            I[aux_index] += V.val
            aux_index += 1

    for Is in I_sources.values():
        r = Is.n1
        c = Is.n2
        if r == c:
            continue
        elif c == 0:
            I[r-1] -= Is.val
        elif r == 0:
            I[c-1] += Is.val
        else:
            I[r-1] -= Is.val
            I[c-1] += Is.val

"""
1.This function solves the equations(matrix problem)
2.Prints the unknowns in somewhat nice format
"""
def Solve():
    solution = np.linalg.solve(G, I)
    print("\n1.The value of unknowns are found in phasors.\n2.The currents through voltage sources are in passive sign convention")
    print("Nodes : ",nodes)
    for i in range(1,len(nodes)-len(Shorts)):
        print("V(",i,") : ",solution[i-1],sep="")
    for short in Shorts:
        for Node in nodes.values():
            if Node == short[1]:
                if short[0] == 0:
                    print("V(",Node,") : ",0,sep="")
                else:
                    print("V(",Node,") : ",solution[Node-1],sep="")

    v = len(nodes) - len(Shorts) - 1
    for Vs in V_sources.keys():
        print("I(",Vs,") : ",solution[v],sep="")
        v += 1


"""
Now I am just calling the different functions in the appropriate order
"""
nodes_and_shorts(w)
Read_Ciruit()
manage_shorts()
order = len(nodes) + len(V_sources) - len(Shorts) - 1
G = np.zeros((order,order),dtype=complex)                  #Making the conductance matrix of zeros of desired order 
I = np.zeros(order,dtype=complex)                          #Making the Source matrix of zeros of desired order
Create_MNA_matrix()
Solve()
