import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from sys import argv
import pickle as pkl

script, globstring = argv

# Create list of the appropriate HOLE files

hole_file_list = glob(globstring)
hole_file_list.sort()

# Load HOLE output files
up_lim  = 64
low_lim = -64
Pore_Radii = []
Pore_Axis  = np.arange(-64,65)

# Extract relevant data from HOLE output files
for hole_file in hole_file_list:
    with open(hole_file) as FileIN:
        temp_radii = []
        for line in FileIN:
            val = line.split()
            if (float(val[0]) <= up_lim and float(val[0]) >= low_lim):
                temp_radii.append(float(val[1]))
        if len(temp_radii) > 0:
            Pore_Radii.append(temp_radii)

# Block Average the data
def BlockAvg(M, RadArr):
    n = len(RadArr)     # number of elements
    bl = int(n/M)       # block length
    cut = n%M
    for i in range(0,cut,1):
        RadArr = np.delete(RadArr, 0, 1)
    # Create list containing blocks
    bList = [[] for x in range(int(M))]
    # Populate each block with 'bl' elements
    for i in range(int(M)):
        for e in range(0,bl,1):
            bList[i].append(RadArr[e])
    AvgList = []
    for i in range(int(M)):
        AvgList[].append(np.mean(bList[i]))
              

# Save Extracted data for future processing
with open(str(globstring + '_data.pkl'), 'wb') as out:
    pkl.dump(Pore_Radii, out)
    pkl.dump(Pore_Axis, out)
