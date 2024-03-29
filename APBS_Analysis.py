import numpy as np
import matplotlib.pyplot as plt
import gridData as gd
from glob import glob
from sys import argv
import pickle as pkl
from tqdm import tqdm
script, globstring, outname, rmin = argv

# Create list of the appropriate volume files

volume_file_list = glob(globstring)
volume_file_list.sort()
# Load volume files
Volume_List = []
for i in tqdm(range(len(volume_file_list))):
        Volume_List.append(gd.Grid(volume_file_list[i]))
# Find center (x,y) of array (i.e. center of the Gap Junction pore – aligned using VMD)
Xo_list = []
Yo_list = []
for den in Volume_List:
        lenx, leny, lenz = den.grid.shape
        Xo_list.append(int(lenx/2))
        Yo_list.append(int(leny/2))
# Find list of all (x,y) pairs that are within core of radius = rmin
rmin = int(rmin)
xmax = int(rmin)
ymax = int(rmin)
x_list = []
y_list = []
for xo,yo in zip(Xo_list,Yo_list):
        x_list_temp = []
        y_list_temp = []
        for x in range(0,xmax + 1,1):
                for y in range(0,ymax + 1,1):
                        if (((x)**2)+((y)**2)) <= (rmin)**2: # This is the equation for all circles with a radii <= rmin
                                x_list_temp.append(xo + x)
                                y_list_temp.append(yo + y)
                        else:
                                pass
        x_list.append(x_list_temp)
        y_list.append(y_list_temp)
# Average the potentials from each point in the circular plane for a given z-value
CenterPots = []
Pore_Axes  = []
denN       = 0
for den in Volume_List:
        x,y,z     = den.edges
        Pore_Axes.append(z[0:-1])
        PotentialTemp = []
        for z in tqdm(range(0,lenz,1)):
                Avg_pot   = 0
                total_pot = 0
                for i in range(0,len(x_list[denN]),1):
                        point_pot = den.grid[x_list[denN][i]][y_list[denN][i]][z]
                        total_pot = total_pot + point_pot
                Avg_pot = total_pot / len(x_list[denN])
                PotentialTemp.append(Avg_pot)
        CenterPots.append(PotentialTemp)
        denN += 1
# Save Extracted data for future processing
with open(str(outname + '_apbs.pkl'), 'wb') as out:
        pkl.dump(CenterPots, out)
        pkl.dump(Pore_Axes[0], out)
