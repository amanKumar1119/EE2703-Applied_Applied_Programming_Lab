"""
Name       : Aman Kumar
Assignment : 1
Date       : 17-02-2021
Inputs     : i) Name of the netlist file as the only command line argument.
            ii) The netlist file.
Output     : i) Circuit defintion printed from bottom to top, right to left excluding comments.
            ii) Omitting any junk other than the circuit definition.
"""
from sys import argv

"""Checking if correct number of inputs are given by the user
through the command line."""
if len(argv) != 2:
    print("\nUsage : %s <InputFileName>" % argv[0])
    exit()

(START,END) = (".circuit",".end")            #Storing important connstants
netlist_name = argv[1]                       #Storing the name of input file provided

"""
  i)Checking if filename given is valid.
 ii)Finding the segment containing the the circuit definition
iii)Checking if the file name given is valid.
"""
try:
    fh = open(netlist_name,"r")             #Trying to open the mentioned file with File Handle "fh"
    lines = fh.readlines()
    fh.close()                              #Closing the file handle "fh"
    (cstart,cend) = (-1,-2)                 #Indexes to identify the segment containing the circuit definition                          
    
    for i in range(len(lines)):
        if START == lines[i][:len(START)]:  #Checking if the line is ".circuit"
            cstart = i
        elif END == lines[i][:len(END)]:    #Checking if the line is ".end"
            cend = i
            break
    
    if cstart >= cend or cstart*cend < 0:
        print("\nInvalid Circuit Definition")
        exit()

except IOError:                             #If the file specified is Invalid and could not be opened
    print("\nCould not open the File mentioned.")
    exit()
    
    
"""
1.Printing the output in the desired format.
i.e. Circuit definition from bottom to top and right to left.
2.Storing the information of the components
"""
#(Nested)Dictionary to store the information of components.
#The keys are the names of the components given in the netlist.
#e.g. if a line in netlist is "V1 1 2 10", then "V1" will be the key that will hold the data for this in the dictionary.
components = {}            

for line in reversed(lines[cstart+1:cend]):
    line = line.split("#")[0].rstrip().split(" ")

    #Checking which component is being described
    if line[0][0] == "R":
        components[line[0]] = {}
        components[line[0]]["component"] = "Resistor"
    elif line[0][0] == "V":
        components[line[0]] = {}
        components[line[0]]["component"] = "Voltage Source"
    elif line[0][0] == "I":
        components[line[0]] = {}
        components[line[0]]["component"] = "Current Source"
    elif line[0][0] == "C":
        components[line[0]] = {}
        components[line[0]]["component"] = "Capacitor"
    elif line[0][0] == "L":
        components[line[0]] = {}
        components[line[0]]["component"] = "Inductor"
    elif line[0][0] == "E":
        components[line[0]] = {}
        components[line[0]]["component"] = "VCVS"
        components[line[0]]["From_node"] =line[1]
        components[line[0]]["To_node"] =line[2]
        components[line[0]]["ctrl_n1"] = line[3]      #Controlling voltage is across "ctrl_n1" and "ctrl_n2"
        components[line[0]]["ctrl_n2"] = line[4]
        components[line[0]]["Value"] =float(line[5])
    elif line[0][0] == "F":
        components[line[0]] = {}
        components[line[0]]["component"] = "CCVS"
        components[line[0]]["From_node"] =line[1]
        components[line[0]]["To_node"] =line[2]
        components[line[0]]["ctrl_Vsource"] = line[3] #Controlling current is through "ctrl_Vsource"
    elif line[0][0] == "G":
        components[line[0]] = {}
        components[line[0]]["component"] = "VCCS"
        components[line[0]]["From_node"] =line[1]
        components[line[0]]["To_node"] =line[2]
        components[line[0]]["ctrl_n1"] = line[3]     #Controlling voltage is across "ctrl_n1" and "ctrl_n2"
        components[line[0]]["ctrl_n2"] = line[4]
        components[line[0]]["Value"] =float(line[5])
    elif line[0][0] == "H":
        components[line[0]] = {}
        components[line[0]]["component"] = "CCCS"
        components[line[0]]["From_node"] =line[1]
        components[line[0]]["To_node"] =line[2]
        components[line[0]]["ctrl_Vsource"] = line[3] #Controlling current is through "ctrl_Vsource"
    else:
        print(line[0],"element not supported") 

    #Storing the From node, To node and value for the component.
    if line[0][0] not in ["E","F","G","H"]:           #For controlled source these values are already stored.
        components[line[0]]["From_node"] =line[1]
        components[line[0]]["To_node"] =line[2]
        components[line[0]]["Value"] =float(line[3])

    #Printing the output in the desired format
    line.reverse()
    print(" ".join(line))
